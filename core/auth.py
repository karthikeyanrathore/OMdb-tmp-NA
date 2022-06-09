from flask import Blueprint, g, request, render_template
from flask import session, redirect, url_for
from flask import Flask
import logging
import functools

from core.db import db
from core.query import insertPerson, authenticatePerson
from core.models import Person

logger = logging.getLogger(f"AUTH .{__name__}")
auth_bp = Blueprint("auth", __name__)


@auth_bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		person = Person.query.filter_by(id=user_id).first()
		g.user = person


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
		return view(**kwargs)
	return wrapped_view

@auth_bp.route("/")
def home():
  return "Auth working :/"


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		uname = request.form['uname']
		password = request.form['password']
		
		if not uname:
			error = "Username is Required"
			logger.error(error)
		elif not password:
			error = "Password is Required"
			logger.error(error)
			
		if error is None:
			success, err = insertPerson(uname, password)
			if not success:
				error = err
				logger.error(error)
			else:
				logger.info("User register OK")
				return redirect(url_for('auth.login'))
		
		# flash(error)
	return render_template("auth/register.html", error=error)
	
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		uname = request.form['uname']
		password = request.form['password']
		
		if not uname:
			error = "Username is Required"
			logger.error(error)
		elif not password:
			error = "Password is Required"
			logger.error(error)
		
		if error is None:
			success, err, user_id = authenticatePerson(uname, password)
			if not success:
				error = err
				logger.error(error)
			else:
				#  session['user_id'] = user_id
				session.clear()
				session['user_id'] = user_id
				logger.info("User login OK")
				return redirect(url_for('search.home'))
		
		# flash(error)
	# if user_id is already stored in session['user_id']
	# redirect it to search.home
	if g.user:
		return redirect(url_for('search.home'))
	return render_template("auth/login.html", error=error)		
				
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
