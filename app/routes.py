from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort
from .forms import DaftarAkunForm, MasukAkunForm, BiodataSiswaForm, DataOrangtuaForm
from .models import Pengguna, Biodata, Orangtua
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/dashboard')
@login_required
def home():
   # foto_profil = url_for('static', filename='img/foto-profil/' + current_user.foto_profil)
   return render_template('index.html', title='PPDB', page='Dasbor', data=Pengguna.query.filter_by(id=current_user.id))

@app.errorhandler(404)
@login_required
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error_page.html', title='Error'), 404

@app.route('/', methods=['GET','POST'])
@app.route('/masuk', methods=['GET','POST'])
def login():
   if current_user.is_authenticated:
        return redirect(url_for('home'))
   form = MasukAkunForm()
   if form.validate_on_submit():
        email = Pengguna.query.filter_by(email=form.email.data).first()
        print(email)
        if email and bcrypt.check_password_hash(email.kata_sandi, form.kata_sandi.data):
            login_user(email, remember=form.remember.data)
            if email.email != 'admin@ppdb.smkn1sentani.sch.id':
               next_page = request.args.get('next')
               return redirect(next_page) if next_page else redirect(url_for('home'))
            elif email.email == 'admin@ppdb.smkn1sentani.sch.id':
               login_user(email, remember=form.remember.data)
               next_page = request.args.get('next')
               return redirect(next_page) if next_page else redirect(url_for('dashboard'))
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


# Biodata Calon Siswa
@app.route('/data/siswa/', methods=['GET','POST'])
@login_required
def lengkapi_biodata():
   form = BiodataSiswaForm(nama_lengkap = current_user.nama_lengkap)
   if form.validate_on_submit():
      biodata = Biodata(nisn=form.nisn.data, jenis_kelamin=form.jenis_kelamin.data, 
                     agama=form.agama.data, asal_smp=form.asal_smp.data, 
                     kompetensi=form.pilihan_jurusan.data, status=form.status_suku.data, pengguna=current_user)
      db.session.add(biodata)
      db.session.commit()
      flash('Biodata berhasil disimpan','success')
      return redirect(url_for('biodata', id=biodata.id))
   return render_template('data_siswa/biodata.html', title='Lengkapi Biodata', page='Biodata', form=form
                     , data=Biodata.query.get(current_user.id))

@app.route('/data/siswa/<id>/edit/', methods=['GET','POST'])
@login_required
def edit_biodata(id):
   data = Biodata.query.get_or_404(id)
   if data.pengguna != current_user:
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
      return redirect(url_for('biodata', id=data.id))
   else:
      form.nisn.data = data.nisn
      form.nama_lengkap.data = current_user.nama_lengkap
      form.jenis_kelamin.data = data.jenis_kelamin 
      form.agama.data = data.agama
      form.asal_smp.data = data.asal_smp
      form.pilihan_jurusan.data = data.kompetensi
      form.status_suku.data = data.status   
   return render_template('data_siswa/biodata.html', title='Biodata', page='Biodata', 
                  form=form, data=data, update='update')


@app.route('/data/siswa/<id>/', methods=['GET','POST'])
@login_required
def biodata(id):
   data = Biodata.query.get_or_404(id)
   if data.pengguna.id != current_user.id:
      abort(404)
   form = BiodataSiswaForm()
   form.nisn.data = data.nisn
   form.nama_lengkap.data = current_user.nama_lengkap
   form.jenis_kelamin.data = data.jenis_kelamin 
   form.agama.data = data.agama
   form.asal_smp.data = data.asal_smp
   form.pilihan_jurusan.data = data.kompetensi
   form.status_suku.data = data.status   
   return render_template('data_siswa/biodata.html', title='Biodata', page='Biodata', 
                  form=form, data=data, biodata='biodata')

# Akhir Biodata Siswa

# Orangtua
@app.route('/data/orangtua/', methods=['GET','POST'])
@login_required
def lengkapi_orangtua():
   form = DataOrangtuaForm()
   if form.validate_on_submit():
      orangtua = Orangtua(no_telepon=form.no_telepon.data, nama_orangtua=form.nama_orangtua.data, 
                     alamat=form.alamat.data, pengguna=current_user)
      db.session.add(orangtua)
      db.session.commit()
      flash('Data orangtua berhasil disimpan','success')
      return redirect(url_for('orangtua', id=orangtua.id))
   return render_template('data_orangtua/index.html', title='Lengkapi Data Orangtua',
                     page='Orangtua', form=form, data=Biodata.query.get(current_user.id))

@app.route('/data/orangtua/<id>/', methods=['GET','POST'])
@login_required
def orangtua(id):
   data = Orangtua.query.get_or_404(id)
   if data.pengguna != current_user:
      abort(404)
   form = DataOrangtuaForm()
   form.no_telepon.data = data.no_telepon
   form.nama_orangtua.data = data.nama_orangtua
   form.alamat.data = data.alamat  
   return render_template('data_orangtua/index.html', title='Orangtua', page='Orangtua', 
                  form=form, data=data, orangtua='orangtua')

@app.route('/data/orangtua/<id>/edit/', methods=['GET','POST'])
@login_required
def edit_orangtua(id):
      data = Orangtua.query.get_or_404(id)
      if data.pengguna != current_user:
         abort(404)
      form = DataOrangtuaForm()
      if form.validate_on_submit():
         data.no_telepon = form.no_telepon.data 
         data.nama_orangtua = form.nama_orangtua.data    
         data.alamat = form.alamat.data  
         db.session.commit()
         flash('Data orangtua berhasil diupdate','success')
         return redirect(url_for('lengkapi_orangtua', id=data.id))
      else:
         form.no_telepon.data = data.no_telepon
         form.nama_orangtua.data = data.nama_orangtua
         form.alamat.data = data.alamat  
      return render_template('data_orangtua/index.html', title='Orangtua', page='Orangtua', 
                     form=form, data=data, update='update')


# Link Sidebar belum fix (kalau user 2 membuat data orangtua deluan, maka itu akan dibaca milik data user 1)
# Perbaiki bagian link (kalau sudah tambah data, tidak boleh masuk halaman itu lagi, harus di redirect ke list data)






# ADMIN DASHBOARD

@app.route('/admin/')
@login_required
def dashboard():
   if current_user.email != "admin@ppdb.smkn1sentani.sch.id":
        return redirect(url_for('home'))
   return render_template('admin.html', title='Admin Dashboard', page='Admin Dasbor' , 
                        biodata=Biodata.query.count(), pengguna=Pengguna.query.order_by('id'))

@app.route('/admin/siswa/')
@login_required
def siswa_biodata():
   return render_template('admin/siswa.html', title="Data Siswa", page='Data Siswa', data=Biodata.query.all())

@app.route('/admin/orangtua/')
@login_required
def orangtua_biodata():
   return render_template('admin/orangtua.html', title="Data Orangtua", page='Data Orangtua', data=Orangtua.query.all())