from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['LOCKER_SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    from .views import main
    app.register_blueprint(main)

    return app
