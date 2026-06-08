from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required, role_required
from helper import Helper
import datetime

from .inventory_api import diagnosa_api
from models import Diagnosa, db, DiagnosaGejala, Pasien


def serialize_diagnosa(diagnosa):
    gejalas = DiagnosaGejala.query.filter_by(diagnosa_id=diagnosa.id).all()
    return {
        "id": diagnosa.id,
        "pasien_id": diagnosa.pasien_id,
        "penyakit_id": diagnosa.penyakit_id,
        "tanggal_diagnosa": diagnosa.tanggal_diagnosa,
        "pasien": {
            "id": diagnosa.pasien.id,
            "nama": diagnosa.pasien.nama,
            "alamat": diagnosa.pasien.alamat,
            "tanggal_lahir": diagnosa.pasien.tanggal_lahir,
            "jenis_kelamin": diagnosa.pasien.jenis_kelamin,
            "nomor_telepon": diagnosa.pasien.nomor_telepon,
        },
        "penyakit": {
            "id": diagnosa.penyakit.id,
            "kode": diagnosa.penyakit.kode,
            "nama": diagnosa.penyakit.nama,
            "bobot": diagnosa.penyakit.bobot,
            "solusi": diagnosa.penyakit.solusi,
        },
        "gejala": [
            {
                "id": gejala_data.gejala.id,
                "kode": gejala_data.gejala.kode,
                "nama": gejala_data.gejala.nama,
                "is_active": gejala_data.gejala.is_active,
            }
            for gejala_data in gejalas
        ],
    }


@diagnosa_api.route("", methods=["GET"])
@auth_required
@role_required("admin")
def get_all_diagnosa():
    diagnosas = Diagnosa.query.all()
    result = [serialize_diagnosa(diagnosa) for diagnosa in diagnosas]
    return {"diagnosas": result}, 200


@diagnosa_api.route("/search", methods=["GET"])
@auth_required
@role_required("admin")
def search_diagnosa():
    mulai = request.args.get("mulai")
    hingga = request.args.get("hingga")

    if not mulai or not hingga:
        return {"error": "Parameter mulai dan hingga wajib diisi"}, 400

    try:
        mulai = datetime.datetime.fromisoformat(mulai)
        hingga = datetime.datetime.fromisoformat(hingga)
    except ValueError:
        return {"error": "Format tanggal tidak valid"}, 400

    diagnosas = Diagnosa.query.filter(
        Diagnosa.tanggal_diagnosa.between(mulai, hingga)
    ).all()
    result = [serialize_diagnosa(diagnosa) for diagnosa in diagnosas]
    return result, 200


@diagnosa_api.route("/<int:diagnosa_id>", methods=["GET"])
@auth_required
@role_required("admin", "pasien")
def get_diagnosa_by_id(diagnosa_id):
    diagnosa = Diagnosa.query.get(diagnosa_id)
    if diagnosa is None:
        return {"error": "Diagnosa tidak ditemukan"}, 404

    current_user = g.current_user
    pasien_milik_user = diagnosa.pasien.user_id == current_user["id"]
    if current_user["role"] == "pasien" and not pasien_milik_user:
        return {"message": "Forbidden"}, 403

    return serialize_diagnosa(diagnosa), 200


@diagnosa_api.route("/", methods=["POST"])
@auth_required
@role_required("pasien")
def create_diagnosa():
    current_user = g.current_user

    pasien = Pasien.query.filter_by(user_id=current_user["id"]).first()
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404

    data = request.get_json()
    penyakit_id = data.get("penyakit_id")
    if not penyakit_id:
        return {"error": "penyakit_id wajib diisi"}, 400

    gejala_items = data.get("gejala", data.get("gejalas", []))

    diagnosa = Diagnosa(
        pasien_id=pasien.id,
        penyakit_id=penyakit_id,
        tanggal_diagnosa=datetime.datetime.now(),
    )

    try:
        db.session.add(diagnosa)
        db.session.flush()
        for gejala in gejala_items:
            gejala_id = gejala.get("gejala_id") if isinstance(gejala, dict) else gejala
            diagnosaGejala = DiagnosaGejala(diagnosa_id=diagnosa.id, gejala_id=gejala_id)
            db.session.add(diagnosaGejala)

        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e, Diagnosa)
        return jsonify({"error": error_msg}), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    return {"message": "Diagnosa berhasil ditambah."}, 201


@diagnosa_api.route("/<int:diagnosa_id>", methods=["PUT"])
@auth_required
@role_required("admin")
def update_diagnosa(diagnosa_id):
    diagnosa = Diagnosa.query.get(diagnosa_id)
    if diagnosa is None:
        return {"error": "Diagnosa tidak ditemukan"}, 404
    data = request.get_json()
    diagnosa.penyakit_id = data.get("penyakit_id", diagnosa.penyakit_id)
    diagnosa.pasien_id = data.get("pasien_id", diagnosa.pasien_id)
    db.session.commit()

    return {"message": "Diagnosa berhasil diubah"}, 200


@diagnosa_api.route("/<int:diagnosa_id>", methods=["DELETE"])
@auth_required
@role_required("admin")
def delete_diagnosa(diagnosa_id):
    diagnosa = Diagnosa.query.get(diagnosa_id)
    if diagnosa is None:
        return {"error": "Diagnosa tidak ditemukan"}, 404
    db.session.delete(diagnosa)
    db.session.commit()
    return {"message": "Diagnosa berhasil dihapus"}, 200
