import os

DEBUG = bool(os.environ.get("FLASK_DEBUG", 0))

SQLALCHEMY_DATABASE_URI="sqlite:///pp.sqlite3"

CURRENT_VERSION_API="v1"

SECRET_KEY=os.environ['SECRET_KEY']

API='https://www.omdbapi.com/'
API_KEY=os.environ['API_KEY']
