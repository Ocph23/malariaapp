from models import Penyakit, db


PENYAKIT_SEEDS = [
    {
        "kode": "P001",
        "nama": "Tropika",
        "bobot": 0.1,
        "solusi": "Cek darah",
    },
    {
        "kode": "P002",
        "nama": "Tersiana",
        "bobot": 0.3,
        "solusi": "Cek Darah",
    },
    {
        "kode": "P003",
        "nama": "Mix Tropika & Tersiana",
        "bobot": 0.3,
        "solusi": "Cek darah",
    },
    {
        "kode": "P004",
        "nama": "Malariae",
        "bobot": 1,
        "solusi": "Cek Darah",
    },
]


def seed_penyakit():
    for item in PENYAKIT_SEEDS:
        penyakit = Penyakit.query.filter_by(kode=item["kode"]).first()
        if penyakit:
            penyakit.nama = item["nama"]
            penyakit.bobot = item["bobot"]
            penyakit.solusi = item["solusi"]
            continue

        db.session.add(Penyakit(**item))

    db.session.commit()
