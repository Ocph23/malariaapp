from flask import request, g, jsonify
from sqlalchemy.exc import IntegrityError
from core import auth_required
from helper import Helper
import datetime

from .inventory_api import diagnosa_api
from models import Diagnosa, db, DiagnosaGejala


@diagnosa_api.route("", methods=["GET"])
@auth_required
def get_all_diagnosa():
    current_user = g.current_user
    print(f"User ID: {current_user}")
    diagnosas = Diagnosa.query.all()

    result = []
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
            "gejala": [],
        }
        for gejalaData in gejala:
            dataDiagnosa["gejala"].append(
                {
                    "id": gejalaData.gejala.id,
                    "kode": gejalaData.gejala.kode,
                    "nama": gejalaData.gejala.nama,
                    "is_active": gejalaData.gejala.is_active,
                }
            )

        result.append(dataDiagnosa)
    return {"diagnosas": result}, 200


@diagnosa_api.route("<int:diagnosa_id>", methods=["GET"])
@auth_required
def get_diagnosa_by_id(diagnosa_id):
    from models import Diagnosa

    diagnosa = Diagnosa.query.get(diagnosa_id)
    if diagnosa is None:
        return {"error": "Diagnosa tidak ditemukan"}, 404
    return {
        "id": diagnosa.id,
        "kode": diagnosa.kode,
        "nama": diagnosa.nama,
        "is_active": diagnosa.is_active,
    }, 200


@diagnosa_api.route("/", methods=["POST"])
@auth_required
def create_diagnosa():
    from models import Diagnosa

    current_user = g.current_user

    pasien = Pasien.query.filter_by(user_id=current_user["id"]).first()
    if pasien is None:
        return {"error": "Pasien tidak ditemukan"}, 404

    data = request.get_json()

    diagnosa = Diagnosa(
        pasien_id=pasien.id,
        tanggal_diagnosa=datetime.datetime.now(),
    )

    try:
        db.session.add(diagnosa)
        db.session.flush()
        for gejala in data["gejala"]:
            diagnosaGejala = DiagnosaGejala(
                diagnosa_id=diagnosa.id, gejala_id=gejala["gejala_id"]
            )
            db.session.add(diagnosaGejala)
            db.session.flush()

        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_msg, status_code = Helper.handle_integrity_error(e, Diagnosa)
        return jsonify({"error": error_msg}), status_code
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    return {"message": "Diagnosa berhasil ditambah."}, 201


@diagnosa_api.route("/<int:diagnosa_id>", methods=["PUT"])
@auth_required
def update_diagnosa(diagnosa_id):
    from models import Diagnosa

    diagnosa = Diagnosa.query.get(diagnosa_id)
    if diagnosa is None:
        return {"error": "Diagnosa tidak ditemukan"}, 404
    data = request.get_json()
    diagnosa.kode = data.get("kode", diagnosa.kode)
    diagnosa.nama = data.get("nama", diagnosa.nama)
    diagnosa.is_active = data.get("is_active", diagnosa.is_active)
    db.session.commit()

    return {"message": "Diagnosa berhasil diubah"}, 200


@diagnosa_api.route("/<int:diagnosa_id>", methods=["DELETE"])
@auth_required
def delete_diagnosa(diagnosa_id):
    from models import Diagnosa

    diagnosa = Diagnosa.query.get(diagnosa_id)
    if diagnosa is None:
        return {"error": "Diagnosa tidak ditemukan"}, 404
    db.session.delete(diagnosa)
    db.session.commit()
    return {"message": "Diagnosa berhasil dihapus"}, 200
