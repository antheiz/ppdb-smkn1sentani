from app import app 
from flask import render_template
from .forms import DaftarAkunForm, MasukAkunForm

@app.route('/dashboard')
def home():
   return render_template('index.html', title='Home')

@app.route('/')
@app.route('/masuk')
def login():
   form = MasukAkunForm()
   return render_template('login.html', form=form)

@app.route('/daftar')
def register():
   form = DaftarAkunForm()
   return render_template('register.html', form=form)