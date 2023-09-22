from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'python flask'
# app.config['SECRET_KEY'] = Config.SECRET_KEY  # Явное присвоение не нужно, если название SECRET_KEY
app.config.from_object(Config)  # Можно использовать следующий вариант
db = SQLAlchemy(app)
"""База данных"""
migrate = Migrate(app, db)
"""Отвечает за миграцию"""
login = LoginManager(app)
"""Отвечает за логины"""
login.login_view = 'login'
""""""

from app import routes, models


