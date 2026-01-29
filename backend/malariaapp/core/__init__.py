from flask import Flask, request, jsonify, g, current_app as app
from functools import wraps
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import os


load_dotenv()
database = SQLAlchemy()
migrate = Migrate()


def create_app():
    print("Initializing core package")
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(os.getenv("FLASK_CONFIG") or "config.DevelopmentConfig")
    init_app(app)
    register_blueprints(app)
    return app


def init_app(app):
    database.init_app(app)
    with app.app_context():
        database.create_all()
    migrate.init_app(app, database)
    import models


def register_blueprints(app: Flask):
    from .blueprints import gejala_api
    from .blueprints import auth_api
    from .blueprints import penyakit_api
    from .blueprints import aturan_api
    from .blueprints import diagnosa_api
    from .blueprints import user_api

    app.register_blueprint(auth_api, url_prefix="/api/auth")
    app.register_blueprint(gejala_api, url_prefix="/api/gejala")
    app.register_blueprint(penyakit_api, url_prefix="/api/penyakit")
    app.register_blueprint(aturan_api, url_prefix="/api/aturan")
    app.register_blueprint(diagnosa_api, url_prefix="/api/diagnosa")
    app.register_blueprint(user_api, url_prefix="/api/user")


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # JWT is expected in the Authorization header: Bearer <token>
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode the token to verify its authenticity and extract payload
            data = jwt.decode(
                token,
                app.config["SECRET_KEY"],
                algorithms="HS256",
            )
            # You can now access the token's data via data['user_id'] or similar
            # and potentially load the full user object if needed.
            g.current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(*args, **kwargs)

    return decorated
