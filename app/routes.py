from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort
from .forms import DaftarAkunForm, MasukAkunForm, BiodataSiswaForm
from .models import Pengguna, Biodata
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/dashboard')
@login_required
def home():
   # foto_profil = url_for('static', filename='img/foto-profil/' + current_user.foto_profil)
   return render_template('index.html', title='PPDB', page='Dasbor', data1=Biodata.query.get(current_user.id))

@app.route('/', methods=['GET','POST'])
@app.route('/masuk', methods=['GET','POST'])
def login():
   if current_user.is_authenticated:
        return redirect(url_for('home'))
   form = MasukAkunForm()
   if form.validate_on_submit():
        email = Pengguna.query.filter_by(email=form.email.data).first()
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
      user = Pengguna(nama_lengkap=form.nama_lengkap.data, email=form.email.data, kata_sandi=hash_pw)
      db.session.add(user)
      db.session.commit()
      flash('Akun berhasil dibuat. Silahkan login', 'success')
      return redirect(url_for('login'))
   return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/biodata/', methods=['GET','POST'])
@login_required
def biodata():
   form = BiodataSiswaForm(nama_lengkap = current_user.nama_lengkap)
   if form.validate_on_submit():
      biodata = Biodata(nisn=form.nisn.data, jenis_kelamin=form.jenis_kelamin.data, 
                     agama=form.agama.data, asal_smp=form.asal_smp.data, 
                     kompetensi=form.pilihan_jurusan.data, status=form.status_suku.data, author=current_user)
      db.session.add(biodata)
      db.session.commit()
      flash('Biodata berhasil disimpan','success')
      return redirect(url_for('edit_biodata', id=biodata.id))
   return render_template('data_siswa/biodata.html', title='Biodata', page='Biodata', form=form, data1=Biodata.query.get(current_user.id))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error_page.html', title='Error', data1=Biodata.query.get(current_user.id)), 404

@app.route('/biodata/<id>/', methods=['GET','POST'])
@login_required
def edit_biodata(id):
      data = Biodata.query.get_or_404(id)
      if data.author != current_user:
         abort(404)
      form = BiodataSiswaForm()
      if form.validate_on_submit():
         data.nisn = form.nisn.data 
         current_user.nama_lengkap = form.nama_lengkap.data    
         data.jenis_kelamin = form.jenis_kelamin.data  
         data.agama = form.agama.data
         data.asal_smp = form.asal_smp.data 
         data.kompetensi = form.pilihan_jurusan.data
         data.status = form.status_suku.data 
         db.session.commit()
         flash('Biodata berhasil diupdate','success')
         return redirect(url_for('edit_biodata', id=data.id))
      else:
         form.nisn.data = data.nisn
         form.nama_lengkap.data = current_user.nama_lengkap
         form.jenis_kelamin.data = data.jenis_kelamin 
         form.agama.data = data.agama
         form.asal_smp.data = data.asal_smp
         form.pilihan_jurusan.data = data.kompetensi
         form.status_suku.data = data.status   
      return render_template('data_siswa/biodata.html', title='Biodata', page='Biodata', 
                     form=form, data=Biodata.query.all(), update='update', data1=Biodata.query.get(current_user.id))