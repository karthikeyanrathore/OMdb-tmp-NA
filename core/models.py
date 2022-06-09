from core.db import db


class Person(db.Model):
  
  __tablename__ = "person"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  playlists = db.relationship('Playlist', backref='person', lazy="subquery")
  
  def __init__(self, name, password):
    self.name = name
    self.password = password

  def __repr__(self):
    return '<Person %r>' % self.name

class Playlist(db.Model):

  __tablename__ = "playlist"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  private = db.Column(db.Boolean, default=False, nullable=False)
  person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
  movies = db.relationship('Movie', backref='playlist', lazy="dynamic")
  
  def __init__(self, name, private):
    self.name = name
    self.private = private

  def __repr__(self):
    return '<Playlist %r>' % self.id


class Movie(db.Model):

  __tablename__ = "movie"

  id = db.Column(db.Integer, primary_key=True)
  omdb_id = db.Column(db.String(50), nullable=False)

  # https://stackoverflow.com/questions/25375179/one-to-many-flask-sqlalchemy
  # https://github.com/karthikeyanrathore/learning/blob/main/book/main.py
  playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
  
  def __init__(self, omdb_id):
    self.omdb_id = omdb_id

  def __repr__(self):
    return '<Movie %r>' % self.id

