from flask import Flask
from config import Config

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'python flask'
# app.config['SECRET_KEY'] = Config.SECRET_KEY  # Явное присвоение не нужно, если название SECRET_KEY
app.config.from_object(Config)  # Можно использовать следующий вариант

from app import routes

pass
