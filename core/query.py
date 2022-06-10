from core.db import db
from core.models import Person, Playlist, Movie 

from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash

def insertPerson(uname, password):
  '''
  >>> from core.db import db
  >>> from core.models import Person
  >>> me = Person('admin', 'admin')
  >>> db.session.add(me)
  >>> db.session.commit()
  >>> Person.query.all()
  [<Person 1>]
  '''
  # storing uname, hash(password)
  me = Person(uname, generate_password_hash(password))
  success = None
  error = None

  try:
    db.session.add(me)
    db.session.commit()
    success = 'success'
  except exc.IntegrityError:
    db.session.rollback()
    error = 'Username already exists'
  except Exception:
    db.session.rollback()
    raise 

  return success, error

def authenticatePerson(uname, password):
  '''
  list(Person.query.filter_by(name=uname).all())
  '''
  person = Person.query.filter_by(name=uname).all()
  success = None
  error = None
  user_id = None

  if len(person) == 0:
    error = 'Username does not exists'
  elif not check_password_hash(person[0].password, password):
    error = 'Incorrect Password'
  else:
    success = 'success'
    user_id = person[0].id
  return success, error, user_id

def insertPlaylist(person, playlist_name, private):
  # check before inserting
  # check if playlist exists or not for the person/user
  success = None
  error = None
  check_person = Person.query.filter_by(id=person.id).first() 
  check_playlists = check_person.playlists
  for playlist in check_playlists:
    if playlist.name == playlist_name:
      error = 'playlist already exists'
      return success, error

  print(person, playlist_name, private)
  if private is False:
    private = False
  else:
    private = True
  p = Playlist(str(playlist_name), private)
  mea = person.playlists.append(p)
  try:
    # db.session.add(mea)
    db.session.commit()
    success = 'success'
  except Exception as e:
    error = e
    db.session.rollback()
    raise 
  
  return success, error 

def insert_Movie_to_playlist(playlist, movie_id):
  success = None
  error = None
  # before insert check if omdb_id is already present or not
  playlist =  (Playlist.query.filter_by(id=playlist.id).first())
  movies = list(playlist.movies)
  
  print("MOVIES", movies)
  for movie in movies:
    if movie.omdb_id == movie_id:
      error = 'Movie already exists in Playlist'
      return success, error

  m = Movie(movie_id)
  playlist.movies.append(m)
  try:
    print('DONE')
    db.session.commit()
    success = 'success'
  except Exception as e:
    error = e
    db.session.rollback()
    raise

  return  success, error






