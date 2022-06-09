from flask import Blueprint, g, request, render_template
from flask import session, redirect, url_for
from flask import Flask
import logging

from core.db import db
from core.auth import login_required
from core.query import insertPlaylist
from core.models import Playlist


logger = logging.getLogger(f"PLAYLIST_HOME .{__name__}")
playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/home')
@login_required
def home():
  # sort: private list first and then ..
  playlists = Playlist.query.filter_by(person_id=g.user.id).order_by(Playlist.private == False).all()
  print(playlists)
  return render_template('playlist/home.html', playlists=playlists)
 
@playlist_bp.route('/home', methods=['GET', 'POST'])
@login_required
def create():
  error = None
  if request.method == 'POST':
    playlist_name = request.form['playlist_name']
    private = False
    print(playlist_name)
    
    if not playlist_name:
      error = 'Playlist Name is Required'
      logger.error(error)
  
    # print(request.form.getlist('private'))
    if len(request.form.getlist('private')) != 0:
      if request.form.getlist('private')[0] == 'TRUE':
        private = True
    
    if error is None:
      success, error = insertPlaylist(g.user, playlist_name.lower(), private)
      if success:
        # i = Playlist.query.filter_by(person_id=g.user.id).all()
        # print(i)
        # return "PLAYLIST ADDED"
        return redirect(url_for('playlist.home'))
        pass
      if error:
        error = "ERROR in creating playlist"
  return render_template('playlist/home.html', error=error)
  

@playlist_bp.route('/<int:user_id>/private/view/<int:playlist_id>', methods=['GET', 'POST'])
@login_required
def view_private_playlist(user_id, playlist_id):
  
  return f'PRIVATE PLAYLIST ID, {playlist_id}'
 

@playlist_bp.route('/<int:user_id>/public/view/<int:playlist_id>', methods=['GET', 'POST'])
def view_public_playlist(user_id, playlist_id):
  
  return f'PUBLIC PLAYLIST ID, {playlist_id}'
  
@playlist_bp.route('<int:user_id>/add/movie/<string:movie_id>', methods=['GET', 'POST'])
@login_required
def add_to_playlist(user_id, movie_id):
  # return f'MOVIE ID, {movie_id}'
  # error = None
  # if request.method == 'POST':
  playlists = Playlist.query.filter_by(person_id=g.user.id).order_by(Playlist.private == False).all()
  return render_template('playlist/add.html', playlists=playlists)
    