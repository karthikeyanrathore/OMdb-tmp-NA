#!/bin/bash
# gunicorn --workers=2 'core.app:create_app()'

if [ ! -d instance ]; then
  mkdir instance
fi

if [[ $DB == 1 ]]; then
  echo "initialize DB"
  rm instance/production.sqlite3
fi

if [[ $ADMIN == 1 ]]; 
then
  echo "RUNNING: admin.app.py"
  export FLASK_APP=admin.app.py
  flask run
else
  echo "RUNNING: core.app:create_app"
  # import env var from .env
  export $(grep -v '^#' .env | xargs)
  echo "API KEY "$API_KEY

  # export FLASK_APP=core.app:create_app
  # export FLASK_ENV=developement
  # export FLASK_DEBUG=1
  # flask run --host "0.0.0.0"
  gunicorn --workers=2 'core.app:create_app()'
fi
