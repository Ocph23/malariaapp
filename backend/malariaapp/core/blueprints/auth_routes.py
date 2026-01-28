from flask import Blueprint, request

from .inventory_api import auth_api
from models import User
import jwt

from werkzeug.security import generate_password_hash, check_password_hash


@auth_api.route('/auth/login', methods=['GET'])
def login():
    from models import User
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user is None:
        return {'error': 'User not found'}, 404

    hash_password = generate_password_hash(data['password'])
    if user.password != hash_password:
        return {'error': 'Invalid password'}, 401
    
    token = jwt.encode(
    {"payload": auth.username},
    "secret",
    algorithm="HS256"
)