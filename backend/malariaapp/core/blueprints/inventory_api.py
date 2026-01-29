from flask import Blueprint

gejala_api = Blueprint("gejala_api", __name__)
auth_api = Blueprint("auth_api", __name__)
penyakit_api = Blueprint("penyakit_api", __name__)
aturan_api = Blueprint("aturan_api", __name__)
diagnosa_api = Blueprint("diagnosa_api", __name__)
user_api = Blueprint("user_api", __name__)

from .gejala_routes import *
from .auth_routes import *
from .penyakit_routes import *
from .aturan_routes import *
from .diagnosa_routes import *
from .user_routes import *
