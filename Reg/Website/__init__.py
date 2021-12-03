from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os.path, sys

db = SQLAlchemy()
DB_NAME = 'database.db'

UPLOAD_FOLDER = os.path.join(sys.path[0],'files')
ALLOWED_EXTENSIONS = {'txt', 'xslx'}


def create_database(app):
    with app.app_context():
        db.create_all(app=app)
        print('Created db!')


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'mariomariomarioa'
    app.config['SQALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Note
    create_database(app)

    return app

