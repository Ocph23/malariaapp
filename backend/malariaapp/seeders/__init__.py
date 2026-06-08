from .user_seeder import seed_user
from .penyakit_seeder import seed_penyakit
from .gejala_seeder import seed_gejala
from .aturan_seeder import seed_aturan

def run_all():
    seed_user()
    seed_penyakit()
    seed_gejala()
    seed_aturan()
