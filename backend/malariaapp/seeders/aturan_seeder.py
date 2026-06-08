from models import Aturan, Gejala, Penyakit, db


ATURAN_SEEDS = [
    ("P001", "G01"),
    ("P001", "G03"),
    ("P001", "G04"),
    ("P001", "G05"),
    ("P001", "G06"),
    ("P001", "G07"),
    ("P002", "G01"),
    ("P002", "G02"),
    ("P002", "G03"),
    ("P002", "G04"),
    ("P002", "G05"),
    ("P002", "G07"),
    ("P003", "G01"),
    ("P003", "G02"),
    ("P003", "G03"),
    ("P003", "G04"),
    ("P003", "G05"),
    ("P003", "G06"),
    ("P003", "G07"),
    ("P003", "G08"),
    ("P004", "G01"),
    ("P004", "G03"),
    ("P004", "G04"),
    ("P004", "G05"),
    ("P004", "G07"),
    ("P004", "G09"),
]


def seed_aturan():
    for penyakit_kode, gejala_kode in ATURAN_SEEDS:
        penyakit = Penyakit.query.filter_by(kode=penyakit_kode).first()
        gejala = Gejala.query.filter_by(kode=gejala_kode).first()

        if not penyakit or not gejala:
            continue

        aturan = Aturan.query.filter_by(
            penyakit_id=penyakit.id,
            gejala_id=gejala.id,
        ).first()

        if aturan:
            aturan.is_active = True
            continue

        db.session.add(
            Aturan(
                penyakit_id=penyakit.id,
                gejala_id=gejala.id,
                is_active=True,
            )
        )

    db.session.commit()
