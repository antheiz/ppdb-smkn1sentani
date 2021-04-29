from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class DaftarAkunForm(FlaskForm):
    nama_depan = StringField('nama_depan', validators=[DataRequired(), Length(max=20, message='Nama depan Wajib di isi')])
    nama_belakang = StringField('nama_belakang', validators=[DataRequired(), Length(max=20, message='Nama belakang Wajib di isi')])
    email = StringField('email', validators=[DataRequired(), Email('Email salah, Silahkan periksa kembali')])
    kata_sandi = PasswordField('kata_sandi', validators=[DataRequired()])
    ulangi_katasandi = PasswordField('ulangi_katasandi', validators=[DataRequired(), EqualTo('kata_sandi', message='Kata sandi salah, Silahkan periksa kembali')])
    daftar = SubmitField('Daftar')


class MasukAkunForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email('Email salah, Silahkan periksa kembali')])
    kata_sandi = PasswordField('kata_sandi', validators=[DataRequired()])
    remember = BooleanField('Simpan kata sandi', default=False)
    masuk = SubmitField('Masuk')