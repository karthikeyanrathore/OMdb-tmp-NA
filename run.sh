#!/bin/bash
# gunicorn --workers=2 'core.app:create_app()'
export FLASK_APP=core.app:create_app
export FLASK_ENV=developement
export FLASK_DEBUG=1
flask run
