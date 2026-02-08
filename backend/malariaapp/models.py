from core import database as db


class Gejala(db.Model):
    __tablename__ = "gejala"
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(100), unique=True, nullable=False)
    nama = db.Column(db.String(200), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)


class Penyakit(db.Model):
    __tablename__ = "penyakit"
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(100), unique=True, nullable=False)
    nama = db.Column(db.String(200), unique=True, nullable=False)
    bobot = db.Column(db.Float, nullable=False)
    solusi = db.Column(db.Text, nullable=False)


class Aturan(db.Model):
    __tablename__ = "aturan"
    id = db.Column(db.Integer, primary_key=True)
    penyakit_id = db.Column(db.Integer, db.ForeignKey("penyakit.id"), nullable=False)
    gejala_id = db.Column(db.Integer, db.ForeignKey("gejala.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    penyakit = db.relationship("Penyakit", backref=db.backref("aturan_list", lazy=True))
    gejala = db.relationship("Gejala", backref=db.backref("aturan_list", lazy=True))


class Pasien(db.Model):
    __tablename__ = "pasien"
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)
    nomor_telepon = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("pasien_list", lazy=True))


class Diagnosa(db.Model):
    __tablename__ = "diagnosa"
    id = db.Column(db.Integer, primary_key=True)
    pasien_id = db.Column(db.Integer, db.ForeignKey("pasien.id"), nullable=False)
    penyakit_id = db.Column(db.Integer, db.ForeignKey("penyakit.id"), nullable=False)
    tanggal_diagnosa = db.Column(db.DateTime, nullable=False)
    pasien = db.relationship("Pasien", backref=db.backref("diagnosa_list", lazy=True))
    penyakit = db.relationship(
        "Penyakit", backref=db.backref("diagnosa_list", lazy=True)
    )


class DiagnosaGejala(db.Model):
    __tablename__ = "diagnosa_gejala"
    id = db.Column(db.Integer, primary_key=True)
    diagnosa_id = db.Column(db.Integer, db.ForeignKey("diagnosa.id"), nullable=False)
    gejala_id = db.Column(db.Integer, db.ForeignKey("gejala.id"), nullable=False)
    gejala = db.relationship(
        "Gejala", backref=db.backref("diagnosa_gejala_list", lazy=True)
    )


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    is_active = db.Column(db.Boolean, default=True)
