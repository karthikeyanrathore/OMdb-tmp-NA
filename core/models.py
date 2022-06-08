from core.db import db


class Person(db.Model):
  
  __tablename__ = "person"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  password = db.Column(db.String(50), nullable=False)
  playlists = db.relationship('Playlist', backref='person', lazy="dynamic")
  
  def __init__(self, name, password):
    self.name = name
    self.password = password

  def __repr__(self):
    return '<Person %r>' % self.id

class Playlist(db.Model):

  __tablename__ = "playlist"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  private = db.Column(db.Boolean, default=False, nullable=False)
  person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)
  songs = db.relationship('Song', backref='playlist', lazy="dynamic")
  
  def __init__(self, name, private, person_id):
    self.name = name
    self.private = private
    self.person_id = person_id

  def __repr__(self):
    return '<Playlist %r>' % self.id


class Song(db.Model):

  __tablename__ = "song"

  id = db.Column(db.Integer, primary_key=True)
  imbd_id = db.Column(db.String(50), nullable=False)
  playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'),nullable=False)
  
  def __init__(self, imbd_id):
    self.imbd_id = imbd_id
    self.playlist_id = playlist_id

  def __repr__(self):
    return '<Song %r>' % self.id

