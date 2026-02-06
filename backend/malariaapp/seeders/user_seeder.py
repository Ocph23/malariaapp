from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


def seed_user():
    password = generate_password_hash("Password@123")
    users = [
        User(
            username="admin", password=password, email="admin@malaria.app", role="admin"
        )
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()
