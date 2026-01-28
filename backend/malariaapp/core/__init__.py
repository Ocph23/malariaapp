from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
database = SQLAlchemy()
migrate = Migrate()
def create_app():
    print("Initializing core package")
    app = Flask(__name__)
    app.config.from_object(os.getenv('FLASK_CONFIG') or 'config.DevelopmentConfig')
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
    app.register_blueprint(gejala_api, url_prefix='/api')
    