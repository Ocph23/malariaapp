from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required
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
    return {"gejalas": result}, 200


@gejala_api.route("<int:gejala_id>", methods=["GET"])
def get_gejala_by_id(gejala_id):
    from models import Gejala

    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {"error": "Gejala not found"}, 404
    return {
        "id": gejala.id,
        "kode": gejala.kode,
        "nama": gejala.nama,
        "is_active": gejala.is_active,
    }, 200


@gejala_api.route("/", methods=["POST"])
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
    return {"message": "Gejala created successfully"}, 201


@gejala_api.route("/<int:gejala_id>", methods=["PUT"])
def update_gejala(gejala_id):
    from models import Gejala

    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {"error": "Gejala not found"}, 404
    data = request.get_json()
    gejala.kode = data.get("kode", gejala.kode)
    gejala.nama = data.get("nama", gejala.nama)
    gejala.is_active = data.get("is_active", gejala.is_active)
    Gejala.save(gejala)
    return {"message": "Gejala updated successfully"}, 200


@gejala_api.route("/<int:gejala_id>", methods=["DELETE"])
def delete_gejala(gejala_id):
    from models import Gejala

    gejala = Gejala.query.get(gejala_id)
    if gejala is None:
        return {"error": "Gejala not found"}, 404
    Gejala.delete(gejala)
    return {"message": "Gejala deleted successfully"}, 200
