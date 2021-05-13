from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, RadioField, SelectField, TextField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import Pengguna
from flask_login import current_user
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))


class DaftarAkunForm(FlaskForm):
    nama_lengkap = StringField('nama_lengkap', validators=[DataRequired(), Length(max=25, message='Nama lengkap tidak sesuai, Silahkan periksa kembali')])
    email = StringField('email', validators=[DataRequired(), Email('Email salah, Silahkan periksa kembali')])
    kata_sandi = PasswordField('kata_sandi', validators=[DataRequired(), Length(min=8, message='Kata sandi minimal 8 Karakter, Silahkan periksa kembali') ])
    ulangi_katasandi = PasswordField('ulangi_katasandi', validators=[DataRequired(), EqualTo('kata_sandi', message='Kata sandi salah, Silahkan periksa kembali'), Length(min=8, message='Kata sandi minimal 8 Karakter, Silahkan periksa kembali')])
    daftar = SubmitField('Daftar')

    def validate_email(self, email):
        pengguna = Pengguna.query.filter_by(email=email.data).first()
        if pengguna:
            raise ValidationError('Email ini sudah pernah terdaftar')


class MasukAkunForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email('Email salah, Silahkan periksa kembali')])
    kata_sandi = PasswordField('kata_sandi', validators=[DataRequired()])
    remember = BooleanField('Simpan kata sandi', default=False)
    masuk = SubmitField('Masuk')

JK = [
    'Laki-laki',
    'Perempuan'
]

JR = [
    'Teknik Komputer dan Jaringan',
    'Teknik Audio Vidio',
    'Teknik Instalasi Tenaga Listrik',
    'Teknik Elektronika Industri',
    'Teknik Kendaraan Ringan',
    'Bisnis Kontruksi dan Properti',
    'Teknik Pengelasan',
    'Teknik dan Bisnis Sepeda Motor',
    'Desain Pemodelan dan Informasi Bangunan'
]

AG = [
    'Kristen',
    'Katolik',
    'Islam',
    'Budha',
    'Hindu'
]

SK = [
    'Orang Asli Papua (OAP)',
    'Non Orang Asli Papua (NON OAP)'
]

class BiodataSiswaForm(FlaskForm):
    nisn = StringField('nisn', validators=[DataRequired(), Length(min=10, message='NISN tidak sesuai. Minimal 10 huruf, silahkan periksa kembali')])
    nama_lengkap = StringField('nama_lengkap', validators=[DataRequired(), Length(max=25, message='Nama lengkap tidak sesuai, Silahkan periksa kembali')])
    jenis_kelamin = RadioField('jenis_kelamin', choices=JK)
    agama = SelectField('agama', choices=AG)
    asal_smp = StringField('asal_smp', validators=[DataRequired(), Length(max=50, message='Asal SMP tidak sesuai, Silahkan periksa kembali')])
    pilihan_jurusan = SelectField('pilihan_jurusan', choices=JR)
    status_suku = RadioField('status_suku', choices=SK)
    simpan = SubmitField('Simpan')

class DataOrangtuaForm(FlaskForm):
    nama_orangtua = StringField('nama_orangtua', validators=[DataRequired(), Length(max=25, message='Nama lengkap tidak sesuai, Silahkan periksa kembali')])
    no_telepon = StringField('nisn', validators=[DataRequired(), Length(min=12, message='No. Telepon tidak sesuai. Minimal 12 angka, silahkan periksa kembali')])
    alamat = TextField('nisn', validators=[DataRequired(), Length(min=30, message='Alamat tidak sesuai. silahkan periksa kembali')])
    simpan = SubmitField('Simpan')