from flask import Blueprint
gejala_api = Blueprint('gejala_api', __name__)
auth_api = Blueprint('auth_api', __name__)

from .gejala_routes import *
from .auth_routes import *


