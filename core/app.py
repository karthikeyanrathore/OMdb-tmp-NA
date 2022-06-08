from flask import Flask, jsonify, make_response, g
import logging

from core import config
from core.db import db
from core.auth import auth_bp

logger = logging.getLogger(f"FASAL_MAIN.{__name__}")

def create_app():
  app = Flask(__name__)
  app.config["DEBUG"] = config.DEBUG
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
  db.init_app(app)
  
  with app.app_context():
    db.create_all()
  ''' 
  @app.before_request
  def create_db_g():
    g.db = db
  '''

  app.register_blueprint(auth_bp, url_prefix="/auth")
  
  return app
