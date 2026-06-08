import os
from sqlalchemy.engine.url import URL

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    url_object = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )
    SQLALCHEMY_DATABASE_URI = url_object
    

class ProductionConfig(Config):
    DEBUG = False   
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
