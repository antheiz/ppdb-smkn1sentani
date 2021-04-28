from app import app 
from flask import render_template

@app.route('/dashboard')
def home():
   return render_template('index.html', title='Home')

@app.route('/')
@app.route('/masuk')
def login():
   return render_template('login.html')

@app.route('/daftar')
def register():
   return render_template('register.html')