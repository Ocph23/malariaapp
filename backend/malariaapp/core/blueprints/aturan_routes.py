from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required, role_required
from helper import Helper

from .inventory_api import aturan_api
from models import Aturan, Penyakit, Gejala, db


@aturan_api.route("", methods=["GET"])
@auth_required
@role_required("admin", "pakar")
def get_all_aturan():
    aturan_list = Aturan.query.filter_by(is_active=True).all()
    result = []

    for aturan in aturan_list:
        result.append(
            {
                "id": aturan.id,
                "penyakit": {
                    "id": aturan.penyakit.id,
                    "kode": aturan.penyakit.kode,
                    "nama": aturan.penyakit.nama,
                },
                "gejala": {
                    "id": aturan.gejala.id,
                    "kode": aturan.gejala.kode,
                    "nama": aturan.gejala.nama,
                },
                "is_active": aturan.is_active,
            }
        )

    return {"aturan": result}, 200


@aturan_api.route("/<int:aturan_id>", methods=["GET"])
@auth_required
@role_required("admin", "pakar")
def get_aturan_by_id(aturan_id):
    aturan = Aturan.query.get(aturan_id)
    if aturan is None:
        return {"error": "Aturan tidak ditemukan"}, 404

    return {
        "id": aturan.id,
        "penyakit_id": aturan.penyakit_id,
        "gejala_id": aturan.gejala_id,
        "is_active": aturan.is_active,
    }, 200


@aturan_api.route("/", methods=["POST"])
@auth_required
@role_required("admin", "pakar")
def create_aturan():
    data = request.get_json()

    # validasi penyakit
    penyakit = Penyakit.query.get(data["penyakit_id"])
    if not penyakit:
        return {"error": "Penyakit tidak ditemukan"}, 404

    # validasi gejala
    gejala = Gejala.query.get(data["gejala_id"])
    if not gejala:
        return {"error": "Gejala tidak ditemukan"}, 404

    aturan = Aturan(
        penyakit_id=data["penyakit_id"],
        gejala_id=data["gejala_id"],
        is_active=data.get("is_active", True),
    )

    try:
        db.session.add(aturan)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e, Aturan)
        return jsonify({"error": error_msg}), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

    return {
        "id": aturan.id,
        "penyakit_id":aturan.penyakit_id,
        "gejala_id":aturan.gejala_id,
        "kode":gejala.kode,
        "nama":gejala.nama,
        "is_active":aturan.is_active
    }, 200


@aturan_api.route("/<int:aturan_id>", methods=["PUT"])
@auth_required
@role_required("admin", "pakar")
def update_aturan(aturan_id):
    aturan = Aturan.query.get(aturan_id)
    if aturan is None:
        return {"error": "Aturan tidak ditemukan"}, 404

    data = request.get_json()

    aturan.penyakit_id = data.get("penyakit_id", aturan.penyakit_id)
    aturan.gejala_id = data.get("gejala_id", aturan.gejala_id)
    aturan.is_active = data.get("is_active", aturan.is_active)

    db.session.commit()
    return {"message": "Aturan berhasil diubah"}, 200


@aturan_api.route("/<int:aturan_id>", methods=["DELETE"])
@auth_required
@role_required("admin", "pakar")
def delete_aturan(aturan_id):
    aturan = Aturan.query.get(aturan_id)
    if aturan is None:
        return {"error": "Aturan tidak ditemukan"}, 404

    aturan.is_active = False
    db.session.commit()

    return {"message": "Aturan berhasil dinonaktifkan"}, 200


@aturan_api.route("/penyakit/<int:penyakit_id>", methods=["GET"])
@auth_required
@role_required("admin", "pakar")
def get_aturan_by_penyakit(penyakit_id):
    aturan_list = Aturan.query.filter_by(penyakit_id=penyakit_id, is_active=True).all()

    result = []
    for aturan in aturan_list:
        result.append(
            {
                "aturan_id": aturan.id,
                "gejala_id": aturan.gejala.id,
                "kode_gejala": aturan.gejala.kode,
                "nama_gejala": aturan.gejala.nama,
            }
        )

    return {"aturan": result}, 200
