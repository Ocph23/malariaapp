from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required
from helper import Helper

from .inventory_api import user_api
from models import User, db


@user_api.route("", methods=["GET"])
@auth_required
def get_all_user():
    current_user = g.current_user
    users = User.query.all()
    result = []
    for user in users:
        result.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            }
        )
    return result, 200


# @user_api.route("<int:user_id>", methods=["GET"])
# @auth_required
# def get_user_by_id(user_id):
#     from models import User

#     user = User.query.get(user_id)
#     if user is None:
#         return {"error": "User tidak ditemukan"}, 404
#     return {
#         "id": user.id,
#         "kode": user.kode,
#         "nama": user.nama,
#         "is_active": user.is_active,
#     }, 200


@user_api.route("/", methods=["POST"])
@auth_required
def create_user():
    from models import User

    data = request.get_json()

    hastPassword = Helper.hash_password("Password@123")
    user = User(
        username=data["username"],
        password=hastPassword,
        email=data["email"],
        role=data["role"],
        is_active=data.get("is_active", True),
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e, User)
        return jsonify({"error": error_msg}), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    return {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "id": user.id,
        "is_active": user.is_active,
    }, 201


@user_api.route("/<int:user_id>", methods=["DELETE"])
@auth_required
def delete_user(user_id):
    from models import User

    user = User.query.get(user_id)
    if user is None:
        return {"error": "User tidak ditemukan"}, 404
    db.session.delete(user)
    db.session.commit()
    return {"message": "User berhasil dihapus"}, 200
