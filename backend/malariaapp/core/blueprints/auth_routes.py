import datetime
from flask import Blueprint, request
from helper import Helper

from .inventory_api import auth_api
from models import User


@auth_api.route("/login", methods=["POST"])
def login():
    from models import User

    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user is None:
        return {"error": "User not found"}, 404
    valid_password = Helper.verify_password(user.password, data["password"])
    print(valid_password)
    if valid_password == False:
        return {"error": "Invalid password"}, 401
    return Helper.generate_token(user)
