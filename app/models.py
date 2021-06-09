from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))


class Pengguna(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    # foto_profil = db.Column(db.String(30), nullable=False, default='defaults.png')
    kata_sandi = db.Column(db.Text, nullable=False)
    biodata = db.relationship('Biodata', backref='pengguna', lazy=True)
    orangtua = db.relationship('Orangtua', backref='pengguna', lazy=True)

class Biodata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nisn = db.Column(db.Integer, nullable=False)
    jenis_kelamin = db.Column(db.String(25), nullable=False)
    agama = db.Column(db.String(25), nullable=False)
    asal_smp = db.Column(db.Text, nullable=False)
    kompetensi = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(25), nullable=False)
    pengguna_id = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)
    

class Orangtua(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ibu = db.Column(db.String(25), nullable=False, default='Tidak ada')
    ayah = db.Column(db.String(25), nullable=False, default='Tidak ada')
    wali = db.Column(db.String(25), nullable=False, default='Tidak ada')
    no_telepon = db.Column(db.Integer, nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    pengguna_id = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)