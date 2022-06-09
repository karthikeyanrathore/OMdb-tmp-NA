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

 




