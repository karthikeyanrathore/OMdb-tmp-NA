import os

DEBUG = bool(os.environ.get("FLASK_DEBUG", 0))

DATABASE=os.path.join('../instance', 'production.sqlite3')

SQLALCHEMY_DATABASE_URI=f'sqlite:///{DATABASE}'

CURRENT_VERSION_API="v1"

SECRET_KEY=os.environ['SECRET_KEY']

API='https://www.omdbapi.com/'
API_KEY=os.environ['API_KEY']
