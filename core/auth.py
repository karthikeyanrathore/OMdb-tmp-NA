from flask import Blueprint, g
from flask import Flask
import logging

from core.db import db

logger = logging.getLogger(f"AUTH .{__name__}")
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
  return "Auth working /"


