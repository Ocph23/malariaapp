from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required
from helper import Helper

from .inventory_api import pasien_api
from models import Pasien, db


@pasien_api.route("", methods=["GET"])
@auth_required
def get_all_pasien():
    current_user = g.current_user
    pasiens = Pasien.query.all()
    result = []
    for pasien in pasiens:
        result.append(
            {
                "id": pasien.id,
                "nama": pasien.nama,
                "alamat": pasien.alamat,
                "tanggal_lahir": pasien.tanggal_lahir.strftime("%Y-%m-%d"),
                "jenis_kelamin": pasien.jenis_kelamin,
                "nomor_telepon": pasien.nomor_telepon,
                "user_id": pasien.user_id,
                "is_active": pasien.is_active,
            }
        )
    return result, 200


@pasien_api.route("<int:pasien_id>", methods=["GET"])
@auth_required
def get_pasien_by_id(pasien_id):
    from models import Pasien

    pasien = Pasien.query.get(pasien_id)
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404
    return {
        "id": pasien.id,
        "nama": pasien.nama,
        "alamat": pasien.alamat,
        "tanggal_lahir": pasien.tanggal_lahir.strftime("%Y-%m-%d"),
        "jenis_kelamin": pasien.jenis_kelamin,
        "nomor_telepon": pasien.nomor_telepon,
        "user_id": pasien.user_id,
        "is_active": pasien.is_active,
    }, 200


@pasien_api.route("/<int:pasien_id>", methods=["PUT"])
@auth_required
def update_pasien(pasien_id):
    from models import Pasien

    pasien = Pasien.query.get(pasien_id)
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404
    data = request.get_json()
    pasien.nama = data.get("nama", pasien.nama)
    pasien.alamat = data.get("alamat", pasien.alamat)
    pasien.tanggal_lahir = data.get("tanggal_lahir", pasien.tanggal_lahir)
    pasien.jenis_kelamin = data.get("jenis_kelamin", pasien.jenis_kelamin)
    pasien.nomor_telepon = data.get("nomor_telepon", pasien.nomor_telepon)
    pasien.is_active = data.get("is_active", pasien.is_active)
    db.session.commit()

    return {"message": "Pasien berhasil diubah"}, 200


@pasien_api.route("/<int:pasien_id>", methods=["DELETE"])
@auth_required
def delete_pasien(pasien_id):
    from models import Pasien

    pasien = Pasien.query.get(pasien_id)
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404

    try:
        db.session.delete(pasien)
        db.session.commit()
        return {"message": "Pasien berhasil dihapus"}, 200

    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e)
        return jsonify(error_msg), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500


@pasien_api.route("/diagnosa", methods=["POST"])
@auth_required
def create_diagnosa():
    from models import Pasien, Diagnosa, Penyakit, Aturan, DiagnosaGejala

    print("Test")
    current_user = g.current_user
    data = request.get_json()
    pasien = Pasien.query.filter_by(user_id=current_user["id"]).first()
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404

    fakta_gejala = [item["kode"] for item in data]

    penyakits = Penyakit.query.all()

    data_penyakit = []
    for penyakit in penyakits:
        aturans = Aturan.query.filter_by(penyakit_id=penyakit.id, is_active=True).all()
        data_penyakit.append(
            {
                "kode": penyakit.kode,
                "nama": penyakit.nama,
                "bobot": penyakit.bobot,
                "solusi": penyakit.solusi,
                "aturan": [aturan.gejala.kode for aturan in aturans],
            }
        )

    hasil = []

    for penyakit in data_penyakit:
        terbukti = backward_chaining(penyakit, fakta_gejala)
        if terbukti:
            hasil.append(
                {
                    "kode": penyakit["kode"],
                    "nama": penyakit["nama"],
                    "bobot": penyakit["bobot"],
                }
            )

    print(hasil)

    return {"message": "Diagnosa berhasil dibuat"}, 201


def backward_chaining(penyakit, fakta_gejala):
    """
    Mengecek apakah suatu penyakit terbukti berdasarkan gejala.
    Optimasi backtracking: berhenti jika satu gejala tidak terpenuhi.
    """
    print()
    print(f"\n🔍 Menguji penyakit: {penyakit}")

    for gejala in penyakit["aturan"]:
        print(f"   ➜ Cek gejala {gejala}")
        if gejala not in fakta_gejala:
            print("   ❌ Gejala tidak terpenuhi → BACKTRACK")
            return False  # 🔥 Backtracking
        print("   ✅ Gejala terpenuhi")
    print("✅ Semua gejala terpenuhi")
    return True
