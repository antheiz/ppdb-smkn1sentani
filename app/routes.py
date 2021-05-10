from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from .forms import DaftarAkunForm, MasukAkunForm, BiodataSiswaForm
from .models import AkunPengguna, BiodataSiswa
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/dashboard')
@login_required
def home():
   # foto_profil = url_for('static', filename='img/foto-profil/' + current_user.foto_profil)
   return render_template('index.html', title='PPDB', page='Dasbor')

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


@app.route('/biodata', methods=['GET','POST'])
def biodata():
   form = BiodataSiswaForm()
   if form.validate_on_submit():
      biodata = BiodataSiswa(nisn=form.nisn.data, nama_lengkap=form.nama_lengkap.data, jenis_kelamin=form.jenis_kelamin.data)
      db.session.add(biodata)
      db.session.commit()
      flash('Biodata berhasil disimpan','success')
      return redirect(url_for('edit_biodata'))
   return render_template('data_siswa/biodata.html', title='Biodata', page='Biodata', form=form)


@app.route('/biodata/<int:id>', methods=['GET','POST'])
@login_required
def edit_biodata(id):
      data = BiodataSiswa.query.get_or_404(id)
      form = BiodataSiswaForm()
      if form.validate_on_submit():
         data.nisn = form.nisn.data 
         data.nama_lengkap = form.nama_lengkap.data    
         data.jenis_kelamin = form.jenis_kelamin.data    
         db.session.commit()
         flash('Biodata berhasil diupdate','success')
         return redirect(url_for('edit_biodata'))
      else:
         form.nisn.data = data.nisn
         form.nama_lengkap.data = data.nama_lengkap
         form.jenis_kelamin.data = data.jenis_kelamin    
      return render_template('data_siswa/biodata.html', title='Biodata', page='Biodata', 
                     form=form, data=BiodataSiswa.query.all())