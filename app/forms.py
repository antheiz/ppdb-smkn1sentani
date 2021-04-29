from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import AkunPengguna

class DaftarAkunForm(FlaskForm):
    nama_lengkap = StringField('nama_lengkap', validators=[DataRequired(), Length(max=40, message='Nama lengkap tidak sesuai, Silahkan periksa kembali')])
    email = StringField('email', validators=[DataRequired(), Email('Email salah, Silahkan periksa kembali')])
    kata_sandi = PasswordField('kata_sandi', validators=[DataRequired(), Length(min=8, message='Kata sandi minimal 8 Karakter, Silahkan periksa kembali') ])
    ulangi_katasandi = PasswordField('ulangi_katasandi', validators=[DataRequired(), EqualTo('kata_sandi', message='Kata sandi salah, Silahkan periksa kembali'), Length(min=8, message='Kata sandi minimal 8 Karakter, Silahkan periksa kembali')])
    daftar = SubmitField('Daftar')

    def validate_email(self, email):
        pengguna = AkunPengguna.query.filter_by(email=email.data).first()
        if pengguna:
            raise ValidationError('Email ini sudah pernah terdaftar')


class MasukAkunForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email('Email salah, Silahkan periksa kembali')])
    kata_sandi = PasswordField('kata_sandi', validators=[DataRequired()])
    remember = BooleanField('Simpan kata sandi', default=False)
    masuk = SubmitField('Masuk')