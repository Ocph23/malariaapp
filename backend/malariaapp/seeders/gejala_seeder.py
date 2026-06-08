from models import Gejala, db


GEJALA_SEEDS = [
    {
        "kode": "G01",
        "nama": "Demam",
        "is_active": True,
    },
    {
        "kode": "G02",
        "nama": "Menggigil",
        "is_active": True,
    },
    {
        "kode": "G03",
        "nama": "Keringat berlebihan",
        "is_active": True,
    },
    {
        "kode": "G04",
        "nama": "Mual dan muntah",
        "is_active": True,
    },
    {
        "kode": "G05",
        "nama": "Lidah pahit",
        "is_active": True,
    },
    {
        "kode": "G06",
        "nama": "Nyeri kepala",
        "is_active": True,
    },
    {
        "kode": "G07",
        "nama": "Nafsu makan menurun",
        "is_active": True,
    },
    {
        "kode": "G08",
        "nama": "Lemas",
        "is_active": True,
    },
    {
        "kode": "G09",
        "nama": "Badan sakit-sakit",
        "is_active": True,
    },
]


def seed_gejala():
    for item in GEJALA_SEEDS:
        gejala = Gejala.query.filter_by(kode=item["kode"]).first()
        if gejala:
            gejala.nama = item["nama"]
            gejala.is_active = item["is_active"]
            continue

        db.session.add(Gejala(**item))

    db.session.commit()
