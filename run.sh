#!/bin/bash
# gunicorn --workers=2 'core.app:create_app()'
if [[ $DB == 1 ]]; then
  echo "initialize DB"
  rm core/pp.sqlite3
fi

# import env var from .env
export $(grep -v '^#' .env | xargs)
echo "API KEY "$API_KEY

export FLASK_APP=core.app:create_app
export FLASK_ENV=developement
export FLASK_DEBUG=1
flask run
