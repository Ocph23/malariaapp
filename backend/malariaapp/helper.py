import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
import datetime
from sqlalchemy.exc import IntegrityError
import re


class Helper:
    def handle_integrity_error(error, model_class):
        """
        Handle IntegrityError dan berikan pesan error yang lebih user-friendly

        Args:
            error: IntegrityError object
            model_class: Class model yang menyebabkan error

        Returns:
            tuple: (error_message, status_code)
        """
        error_str = str(error.orig)

        # Pattern matching untuk unique constraint
        patterns = {
            r"Key \((.*?)\)=\((.*?)\) already exists": lambda m: f"Data dengan {m.group(1)} '{m.group(2)}' sudah terdaftar",
            r'duplicate key value violates unique constraint "(.*?)"': lambda m: f"Data sudah terdaftar di sistem",
            r"violates foreign key constraint": lambda m: "Referensi data tidak valid",
        }

        for pattern, message_func in patterns.items():
            match = re.search(pattern, error_str)
            if match:
                return message_func(match), 409

        # Default message
        return "Terjadi kesalahan pada database", 500

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password, method="sha256")

    @staticmethod
    def verify_password(hash, password):
        return check_password_hash(hash, password)

    @staticmethod
    def generate_token(user):
        payload = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        }

        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return {"token": token, "username": user.username, "role": user.role}, 200

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        except Exception as e:
            return {"error": str(e)}, 401

    @staticmethod
    def refresh_token(old_token):
        try:
            # Decode the old token to get user information
            old_payload = jwt.decode(
                old_token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )

            # Update expiration time
            old_payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=1)

            # Create a new token with updated payload
            new_token = jwt.encode(
                old_payload, app.config["SECRET_KEY"], algorithm="HS256"
            )
            return new_token
        except jwt.ExpiredSignatureError:
            print("Old token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid old token.")
