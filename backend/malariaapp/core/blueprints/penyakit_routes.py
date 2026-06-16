from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required, role_required
from helper import Helper

from .inventory_api import penyakit_api
from models import Penyakit, db


@penyakit_api.route("", methods=["GET"])
@auth_required
def get_all_penyakit():
    current_user = g.current_user
    print(f"User ID: {current_user}")
    penyakits = Penyakit.query.all()
    result = []
    for penyakit in penyakits:
        result.append(
            {
                "id": penyakit.id,
                "kode": penyakit.kode,
                "nama": penyakit.nama,
                "bobot": penyakit.bobot,
                "solusi": penyakit.solusi,
            }
        )
    return result, 200


@penyakit_api.route("/<int:penyakit_id>", methods=["GET"])
@auth_required
def get_penyakit_by_id(penyakit_id):
    from models import Penyakit, Aturan

    penyakit = Penyakit.query.get(penyakit_id)
    if penyakit is None:
        return {"error": "Penyakit tidak ditemukan"}, 404

    aturans = Aturan.query.filter_by(penyakit_id=penyakit_id, is_active=True).all()
    result = []
    for aturan in aturans:
        result.append(
            {
                "id": aturan.id,
                "kode": aturan.gejala.kode,
                "nama": aturan.gejala.nama,
                "gejala_id": aturan.gejala_id,
            }
        )

    return {
        "id": penyakit.id,
        "kode": penyakit.kode,
        "nama": penyakit.nama,
        "bobot": penyakit.bobot,
        "solusi": penyakit.solusi,
        "aturan": result,
    }, 200


@penyakit_api.route("/", methods=["POST"])
@auth_required
@role_required("admin", "pakar")
def create_penyakit():
    from models import Penyakit

    data = request.get_json()
    penyakit = Penyakit(
        kode=data["kode"],
        nama=data["nama"],
        bobot=data["bobot"],
        solusi=data["solusi"],
    )

    try:
        db.session.add(penyakit)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e)
        return jsonify(error_msg), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    return {
        "id": penyakit.id,
        "kode": penyakit.kode,
        "nama": penyakit.nama,
        "bobot": penyakit.bobot,
        "solusi": penyakit.solusi,
    }, 200


@penyakit_api.route("/<int:penyakit_id>", methods=["PUT"])
@auth_required
@role_required("admin", "pakar")
def update_penyakit(penyakit_id):
    from models import Penyakit

    penyakit = Penyakit.query.get(penyakit_id)
    if penyakit is None:
        return {"error": "Penyakit tidak ditemukan"}, 404
    data = request.get_json()
    penyakit.kode = data.get("kode", penyakit.kode)
    penyakit.nama = data.get("nama", penyakit.nama)
    penyakit.bobot = data.get("bobot", penyakit.bobot)
    penyakit.solusi = data.get("solusi", penyakit.solusi)
    db.session.commit()

    return {"message": "Penyakit berhasil diubah"}, 200


@penyakit_api.route("/<int:penyakit_id>", methods=["DELETE"])
@auth_required
@role_required("admin", "pakar")
def delete_penyakit(penyakit_id):
    from models import Aturan, Diagnosa, Penyakit

    penyakit = Penyakit.query.get(penyakit_id)
    if penyakit is None:
        return {"error": "Penyakit tidak ditemukan"}, 404

    aturan_count = Aturan.query.filter_by(penyakit_id=penyakit_id).count()
    diagnosa_count = Diagnosa.query.filter_by(penyakit_id=penyakit_id).count()

    if aturan_count > 0 or diagnosa_count > 0:
        messages = []
        if aturan_count > 0:
            messages.append("masih memiliki relasi aturan")
        if diagnosa_count > 0:
            messages.append("masih digunakan pada riwayat diagnosa")
        return {
            "error": (
                "Penyakit tidak dapat dihapus karena "
                + " dan ".join(messages)
                + ". Hapus data terkait terlebih dahulu."
            )
        }, 409

    try:
        db.session.delete(penyakit)
        db.session.commit()
        return {"message": "Penyakit berhasil dihapus"}, 200
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e, Penyakit)
        return jsonify({"error": error_msg}), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


###Fungsi Backward Chaining + Backtracking
def backwardChaining(gejala):
    from models import Penyakit, Aturan, DiagnosaGejala

    penyakits = Penyakit.query.all()
    for penyakit in penyakits:
        aturan = Aturan.query.filter_by(penyakit_id=penyakit.id, is_active=True).all()
        for aturanData in aturan:
            gejalaData = DiagnosaGejala.query.filter_by(
                diagnosa_id=gejala, gejala_id=aturanData.gejala_id
            )
