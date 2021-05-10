from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return AkunPengguna.query.get(int(user_id))


class AkunPengguna(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama_lengkap = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    foto_profil = db.Column(db.String(30), nullable=False, default='defaults.png')
    kata_sandi = db.Column(db.Text, nullable=False)


class BiodataSiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nisn = db.Column(db.Integer, nullable=False)
    nama_lengkap = db.Column(db.String(25), nullable=False)
    jenis_kelamin = db.Column(db.String(25), nullable=False)