import sqlite3
import os
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from core.models import Person, Playlist, Movie

app = Flask(__name__)


app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

DATABASE= os.path.join('../instance', 'production.sqlite3')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}' 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# https://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database
db = SQLAlchemy(app)

admin = Admin(app, name='OMdb-admin', template_mode='bootstrap3')

admin.add_view(ModelView(Person, db.session))
admin.add_view(ModelView(Playlist, db.session))
admin.add_view(ModelView(Movie, db.session))

