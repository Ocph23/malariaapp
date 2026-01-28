from core import database as db

class Category(db.Model):
     __tablename__ = 'categories'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), unique=True, nullable=False)
     slug = db.Column(db.String(200), unique=True, nullable=False)
     is_active = db.Column(db.Boolean, default=True)
     
class Gejala(db.Model):
     __tablename__ = 'gejala'
     id = db.Column(db.Integer, primary_key=True)
     kode = db.Column(db.String(100), unique=True, nullable=False)
     nama = db.Column(db.String(200), unique=True, nullable=False)
     is_active = db.Column(db.Boolean, default=True)
     
class Penyakit(db.Model):
     __tablename__ = 'penyakit'
     id = db.Column(db.Integer, primary_key=True)
     kode = db.Column(db.String(100), unique=True, nullable=False)
     nama = db.Column(db.String(200), unique=True, nullable=False)
     bobot = db.Column(db.Float, nullable=False)
     solusi = db.Column(db.Text, nullable=False)
     
class Aturan(db.Model):
     __tablename__ = 'aturan'
     id = db.Column(db.Integer, primary_key=True)
     penyakit_id = db.Column(db.Integer, db.ForeignKey('penyakit.id'), nullable=False)
     gejala_id = db.Column(db.Integer, db.ForeignKey('gejala.id'), nullable=False)
     is_active = db.Column(db.Boolean, default=True)
     penyakit = db.relationship('Penyakit', backref=db.backref('aturan_list', lazy=True))
     gejala = db.relationship('Gejala', backref=db.backref('aturan_list', lazy=True))

class User(db.Model):
     __tablename__ = 'users'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(100), unique=True, nullable=False)
     password = db.Column(db.String(200), nullable=False)
     email = db.Column(db.String(200), unique=True, nullable=False)
     role = db.Column(db.String(50), nullable=False, default='user')
     is_active = db.Column(db.Boolean, default=True)


     
     
     
     
     
     