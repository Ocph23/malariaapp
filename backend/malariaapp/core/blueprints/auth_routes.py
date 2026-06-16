import datetime
import jwt
from flask import Blueprint, request, jsonify, g, current_app as app
from helper import Helper
from core import auth_required
from models import db, User
from .inventory_api import auth_api
from models import User, Pasien
from sqlalchemy import or_


@auth_api.route("/login", methods=["POST"])
def login():
    from models import User

    data = request.get_json()
    user = User.query.filter(
        or_(User.username == data["username"], User.email == data["username"])
    ).first()
    if user is None:
        return {"error": "User not found"}, 404
    
    # if user.is_active and user. == False:
    #     return {"error": "User tidak aktif"}, 403

    valid_password = Helper.verify_password(user.password, data["password"])
    print(valid_password)
    if valid_password == False:
        return {"error": "Invalid password"}, 401

    if user.role == "pasien":
        pasien = Pasien.query.filter_by(user_id=user.id).first()
        if pasien is None:
            return {
                "error": "Profil pasien belum lengkap",
                "message": "Akun pasien ini belum memiliki data pasien. Daftar melalui halaman register pasien atau lengkapi data pasien di database.",
            }, 409

    token = Helper.generate_token(user)
    return {
        "token": token,
        "user": {
            "username": user.username,
            "email": user.email,
            "role": user.role,
        },
    }, 200


@auth_api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    passwordHash = Helper.hash_password(data["password"])
    try:
        user = User(
            username=data["username"],
            password=passwordHash,
            email=data["email"],
            role="pasien",
            is_active=True,
        )
        db.session.add(user)
        db.session.flush()
        print(user.id)
        pasien = Pasien(
            user_id=user.id,
            nama=data["nama"],
            alamat=data["alamat"],
            tanggal_lahir=data["tanggal_lahir"],
            jenis_kelamin=data["jenis_kelamin"],
            nomor_telepon=data["nomor_telepon"],
        )
        db.session.add(pasien)
        db.session.commit()

        token = Helper.generate_token(user)
        return {
            "token": token,
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


@auth_api.route("/refresh_token", methods=["POST"])
def refresh_token():
    data = request.get_json()
    token = data["token"]
    new_token = Helper.refresh_token(token)
    return {"token": new_token}, 200


@auth_api.route("/pasien", methods=["GET"])
@auth_required
def get_profile():
    from models import User

    token = None
    # JWT is expected in the Authorization header: Bearer <token>

    # Ambil user dari DB
    user = User.query.get(g.current_user["id"])
    if not user:
        return jsonify({"message": "User not found"}), 404

    g.current_user = user

    pasien = Pasien.query.filter_by(user_id=user.id).first()
    if not pasien:
        return jsonify({"message": "Pasien not found"}), 404

    return (
        jsonify(
            {
                "id": pasien.id,
                "nama": pasien.nama,
                "alamat": pasien.alamat,
                "tanggal_lahir": pasien.tanggal_lahir,
                "jenis_kelamin": pasien.jenis_kelamin,
                "nomor_telepon": pasien.nomor_telepon,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            }
        ),
        200,
    )
