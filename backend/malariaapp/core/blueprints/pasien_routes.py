import datetime
from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required
from helper import Helper

from .inventory_api import pasien_api
from models import DiagnosaGejala, Pasien, db


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


@pasien_api.route("/riwayat", methods=["GET"])
@auth_required
def get_riwayat_diagnosa():
    from models import Pasien, Diagnosa, Penyakit, Aturan, DiagnosaGejala

    current_user = g.current_user
    pasien = Pasien.query.filter_by(user_id=current_user["id"]).first()
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404

    try:
        result = []
        diagnosas = Diagnosa.query.filter_by(pasien_id=pasien.id).all()
        for diagnosa in diagnosas:
            gejala = DiagnosaGejala.query.filter_by(diagnosa_id=diagnosa.id).all()
            dataDiagnosa = {
                "id": diagnosa.id,
                "pasien_id": diagnosa.pasien_id,
                "tanggal_diagnosa": diagnosa.tanggal_diagnosa,
                "pasien": {
                    "id": diagnosa.pasien.id,
                    "nama": diagnosa.pasien.nama,
                    "alamat": diagnosa.pasien.alamat,
                    "tanggal_lahir": diagnosa.pasien.tanggal_lahir,
                    "jenis_kelamin": diagnosa.pasien.jenis_kelamin,
                    "nomor_telepon": diagnosa.pasien.nomor_telepon,
                },
                "penyakit": {
                    "id": diagnosa.penyakit.id,
                    "kode": diagnosa.penyakit.kode,
                    "nama": diagnosa.penyakit.nama,
                    "bobot": diagnosa.penyakit.bobot,
                    "solusi": diagnosa.penyakit.solusi,
                },
                "gejala": [],
            }
            for gejalaData in gejala:
                dataDiagnosa["gejala"].append(
                    {
                        "id": gejalaData.gejala.id,
                        "kode": gejalaData.gejala.kode,
                        "nama": gejalaData.gejala.nama,
                    }
                )
            result.append(dataDiagnosa)

        return result, 201
    except Exception as e:
        return {"error": str(e)}, 500


@pasien_api.route("/savediagnosa", methods=["POST"])
@auth_required
def save_diagnosa():
    from models import Diagnosa

    data = request.get_json()
    current_user = g.current_user

    pasien = Pasien.query.filter_by(user_id=current_user["id"]).first()
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404

    diagnosa = Diagnosa(
        pasien_id=pasien.id,
        penyakit_id=data["penyakit_id"],
        tanggal_diagnosa=datetime.datetime.now(),
    )

    try:
        db.session.add(diagnosa)
        db.session.flush()
        for gejala in data["gejalas"]:
            diagnosaGejala = DiagnosaGejala(diagnosa_id=diagnosa.id, gejala_id=gejala)
            db.session.add(diagnosaGejala)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e, Diagnosa)
        return jsonify({"error": error_msg}), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    return {"message": "Diagnosa berhasil ditambah."}, 201


@pasien_api.route("/diagnosa", methods=["POST"])
@auth_required
def create_diagnosa():
    from models import Pasien, Diagnosa, Penyakit, Aturan, DiagnosaGejala

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
                "id": penyakit.id,
                "kode": penyakit.kode,
                "nama": penyakit.nama,
                "bobot": penyakit.bobot,
                "solusi": penyakit.solusi,
                "aturan": [
                    {
                        "id": aturan.id,
                        "gejala_id": aturan.gejala_id,
                        "kode": aturan.gejala.kode,
                        "nama": aturan.gejala.nama,
                    }
                    for aturan in aturans
                ],
            }
        )

    hasil = []

    for penyakit in data_penyakit:
        pengecekan, status = backward_chaining(penyakit, fakta_gejala)
        hasil.append(
            {
                "id": penyakit["id"],
                "kode": penyakit["kode"],
                "nama": penyakit["nama"],
                "bobot": penyakit["bobot"],
                "pengecekan": pengecekan,
                "status": status,
            }
        )
    return hasil, 201


def backward_chaining(penyakit, fakta_gejala):
    """
    Mengecek apakah suatu penyakit terbukti berdasarkan gejala.
    Optimasi backtracking: berhenti jika satu gejala tidak terpenuhi.
    """
    print()
    print(f"\n🔍 Menguji penyakit: {penyakit}")

    pengecekan = []

    for gejala in penyakit["aturan"]:
        print(f"   ➜ Cek gejala {gejala}")
        if gejala["kode"] not in fakta_gejala:
            pengecekan.append({"gejala": gejala, "status": "BACKTRACK"})
            print("   ❌ Gejala tidak terpenuhi → BACKTRACK")
            return (pengecekan, False)  # 🔥 Backtracking
        pengecekan.append({"gejala": gejala, "status": "TERPENUHI"})
        print("   ✅ Gejala terpenuhi")
    print("✅ Semua gejala terpenuhi")
    return (pengecekan, True)
