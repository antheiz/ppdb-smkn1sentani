from flask import Flask

app = Flask(__name__)
app.secret_key = 'ioafhwa97e9032iakdnwi'

from app import routes