import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
import datetime
from sqlalchemy.exc import IntegrityError
import re


class Helper:
    def handle_integrity_error(error):
        """
        Decorator untuk menangani database errors secara otomatis
        """
        error_msg = str(error.orig) if hasattr(error, "orig") else str(error)

        # PostgreSQL errors
        if "null value in column" in error_msg:
            # Extract column name from error message
            import re

            match = re.search(r'column "(.+?)"', error_msg)
            column = match.group(1) if match else "unknown"
            return {
                "error": "Null value not allowed",
                "message": f"Column '{column}' cannot be null",
                "detail": "Please provide a value for all required fields",
            }, 400

        elif "violates not-null constraint" in error_msg:
            match = re.search(r'column "(.+?)"', error_msg)
            column = match.group(1) if match else "unknown"
            return {
                "error": "Required field missing",
                "message": f"Field '{column}' is required",
                "detail": "This field must be provided",
            }, 400

        elif "violates foreign key constraint" in error_msg:
            match = re.search(r"Key \(.+?\)=\((.+?)\)", error_msg)
            value = match.group(1) if match else "unknown"

            if "is not present in table" in error_msg:
                table_match = re.search(r'table "(.+?)"', error_msg)
                table = table_match.group(1) if table_match else "unknown"
                return {
                    "error": "Reference error",
                    "message": f"Referenced data not found in table '{table}'",
                    "detail": f"The value '{value}' does not exist in the referenced table",
                }, 404

            return {
                "error": "Foreign key violation",
                "message": "The referenced data does not exist",
                "detail": "Please check that all referenced IDs exist in their respective tables",
            }, 400

        elif "duplicate key value violates unique constraint" in error_msg:
            match = re.search(r"Key \((.+?)\)", error_msg)
            column = match.group(1) if match else "unknown"
            value_match = re.search(r"Detail: Key \((.+?)\)=\((.+?)\)", error_msg)

            if value_match:
                key_value = value_match.group(2)
                return {
                    "error": "Duplicate entry",
                    "message": f"Value '{key_value}' already exists for field '{column}'",
                    "detail": "This value must be unique",
                }, 409

            return {
                "error": "Duplicate entry",
                "message": f"A record with this value already exists for {column}",
                "detail": "Please use a unique value",
            }, 409

        elif "value too long for type" in error_msg:
            match = re.search(r"type character varying\((\d+)\)", error_msg)
            max_length = match.group(1) if match else "unknown"
            return {
                "error": "Value too long",
                "message": f"Input exceeds maximum length of {max_length} characters",
                "detail": "Please shorten the input",
            }, 400

        # MySQL errors
        elif "1062" in error_msg or "Duplicate entry" in error_msg:
            return {
                "error": "Duplicate entry",
                "message": "A record with this value already exists",
                "detail": "Please use a unique value",
            }, 409

        elif "1452" in error_msg or "Cannot add or update" in error_msg:
            return {
                "error": "Foreign key constraint fails",
                "message": "Referenced data does not exist",
                "detail": "Please check the referenced IDs",
            }, 400

        # Generic error
        return {
            "error": "Database integrity error",
            "message": "A database constraint was violated",
            "detail": error_msg,
        }, 400

        @staticmethod
        def hash_password(password):
            return generate_password_hash(password)

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
            return token

        @staticmethod
        def verify_token(token):
            try:
                payload = jwt.decode(
                    token, app.config["SECRET_KEY"], algorithms=["HS256"]
                )
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
                old_payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
                    days=1
                )

                # Create a new token with updated payload
                new_token = jwt.encode(
                    old_payload, app.config["SECRET_KEY"], algorithm="HS256"
                )
                return new_token
            except jwt.ExpiredSignatureError:
                print("Old token has expired.")
            except jwt.InvalidTokenError:
                print("Invalid old token.")
