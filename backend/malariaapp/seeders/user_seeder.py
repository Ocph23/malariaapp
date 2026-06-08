from models import db, User
from werkzeug.security import generate_password_hash


def seed_user():
    existing_admin = User.query.filter_by(username="admin").first()
    if existing_admin:
        return

    password = generate_password_hash("Password@123")
    admin = User(
        username="admin", password=password, email="admin@malaria.app", role="admin"
    )
    db.session.add(admin)
    db.session.commit()
