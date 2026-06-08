from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required, role_required
from helper import Helper

from .inventory_api import gejala_api
from models import Gejala, db


@gejala_api.route("", methods=["GET"])
@auth_required
def get_all_gejala():
    current_user = g.current_user
    print(f"User ID: {current_user}")
    gejalas = Gejala.query.all()
    result = []
    for gejala in gejalas:
        result.append(
            {
                "id": gejala.id,
                "kode": gejala.kode,
                "nama": gejala.nama,
                "is_active": gejala.is_active,
            }
        )
    return result, 200


@gejala_api.route("/<int:gejala_id>", methods=["GET"])
@auth_required
def get_gejala_by_id(gejala_id):
    from models import Gejala

    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {"error": "Gejala tidak ditemukan"}, 404
    return {
        "id": gejala.id,
        "kode": gejala.kode,
        "nama": gejala.nama,
        "is_active": gejala.is_active,
    }, 200


@gejala_api.route("/", methods=["POST"])
@auth_required
@role_required("admin", "pakar")
def create_gejala():
    from models import Gejala

    data = request.get_json()
    gejala = Gejala(
        kode=data["kode"], nama=data["nama"], is_active=data.get("is_active", True)
    )

    try:
        db.session.add(gejala)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e, Gejala)
        return jsonify({"error": error_msg}), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

    return {
        "id": gejala.id,
        "kode": gejala.kode,
        "nama": gejala.nama,
        "is_active": gejala.is_active,
    }, 201


@gejala_api.route("/<int:gejala_id>", methods=["PUT"])
@auth_required
@role_required("admin", "pakar")
def update_gejala(gejala_id):
    from models import Gejala

    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {"error": "Gejala tidak ditemukan"}, 404
    data = request.get_json()
    gejala.kode = data.get("kode", gejala.kode)
    gejala.nama = data.get("nama", gejala.nama)
    gejala.is_active = data.get("is_active", gejala.is_active)
    db.session.commit()

    return {"message": "Gejala berhasil diubah"}, 200


@gejala_api.route("/<int:gejala_id>", methods=["DELETE"])
@auth_required
@role_required("admin", "pakar")
def delete_gejala(gejala_id):
    from models import Gejala

    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {"error": "Gejala tidak ditemukan"}, 404

    try:
        db.session.delete(gejala)
        db.session.commit()
        return {"message": "Gejala berhasil dihapus"}, 200

    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e)
        return jsonify(error_msg), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
