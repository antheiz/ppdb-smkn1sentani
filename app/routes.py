from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from .forms import DaftarAkunForm, MasukAkunForm
from .models import AkunPengguna
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/dashboard')
@login_required
def home():
   foto_profil = url_for('static', filename='img/foto-profil/' + current_user.foto_profil)
   return render_template('index.html', title='PPDB', foto_profil=foto_profil)

@app.route('/', methods=['GET','POST'])
@app.route('/masuk', methods=['GET','POST'])
def login():
   if current_user.is_authenticated:
        return redirect(url_for('home'))
   form = MasukAkunForm()
   if form.validate_on_submit():
        email = AkunPengguna.query.filter_by(email=form.email.data).first()
        if email and bcrypt.check_password_hash(email.kata_sandi, form.kata_sandi.data):
            login_user(email, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Email atau kata sandi salah <br> Silahkan periksa kembali','danger')
   return render_template('login.html', title='Login', form=form)

@app.route('/daftar', methods=['GET','POST'])
def register():
   if current_user.is_authenticated:
        return redirect(url_for('home'))
   form = DaftarAkunForm()
   if form.validate_on_submit():
      hash_pw = bcrypt.generate_password_hash(form.kata_sandi.data).decode('utf-8')
      user = AkunPengguna(nama_lengkap=form.nama_lengkap.data, email=form.email.data, kata_sandi=hash_pw)
      db.session.add(user)
      db.session.commit()
      flash('Akun berhasil dibuat. Silahkan login', 'success')
      return redirect(url_for('login'))
   return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))