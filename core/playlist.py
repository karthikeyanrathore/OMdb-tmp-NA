from flask import Blueprint, g, request, render_template
from flask import session, redirect, url_for
from flask import Flask
import logging

from core.db import db
from core.auth import login_required
from core.query import insertPlaylist, insert_Movie_to_playlist, valid_playlist
from core.models import Playlist
from core.ombd import get_movie


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
  playlists = Playlist.query.filter_by(person_id=g.user.id).order_by(Playlist.private == False).all()
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
        render_template('playlist/home.html', error=error, playlists=playlists)
  return render_template('playlist/home.html', playlists=playlists, error=error)
  

# show movies of PRIVATE PLAYLIST
@playlist_bp.route('/<int:user_id>/private/view/<int:playlist_id>', methods=['GET', 'POST'])
@login_required
def view_private_playlist(user_id, playlist_id):
  
  #return f'PRIVATE PLAYLIST ID, {playlist_id}'
  playlist = Playlist.query.filter_by(person_id=user_id, id=playlist_id).first()
  # print(playlist.movies)
  movies = list(playlist.movies)
  # print(movies)
  movies_arr = []
  for movie in movies:
    print("MOVIE ID: ", movie.omdb_id)
    movie = get_movie(movie=movie.omdb_id, apply_filter='ID')
    movies_arr.append(movie)
  return render_template('playlist/private.html', playlist=playlist, movies_arr=movies_arr)
 

# show movies of PUBLIC PLAYLIST
@playlist_bp.route('/<int:user_id>/public/view/<int:playlist_id>')
def view_public_playlist(user_id, playlist_id):
  
  # return f'PUBLIC PLAYLIST ID, {playlist_id}'
  playlist = Playlist.query.filter_by(person_id=user_id, id=playlist_id).first()
  # print(playlist.movies)
  movies = list(playlist.movies)
  # print(movies)
  movies_arr = []
  for movie in movies:
    print("MOVIE ID: ", movie.omdb_id)
    movie = get_movie(movie=movie.omdb_id, apply_filter='ID')
    movies_arr.append(movie)
  return render_template('playlist/public.html', playlist=playlist, movies_arr=movies_arr)
  
@playlist_bp.route('<int:user_id>/add/movie/<string:movie_id>', methods=['GET', 'POST'])
@login_required
def add_to_playlist(user_id, movie_id):
  # return f'MOVIE ID, {movie_id}'
  # error = None
  # if request.method == 'POST':
  movies = get_movie(movie=movie_id, apply_filter='ID')
  movie_name = movies[0]['Title']
  print("MOVIE NAME", movie_name)
  playlists = Playlist.query.filter_by(person_id=g.user.id).order_by(Playlist.private == False).all()
  
  if request.method == 'POST':
    already_exists_playlist = []
    for playlist in playlists:
      success = None
      error = None
       # check if playlists.selected is valid or not
      if len(request.form.getlist(playlist.name)) > 0:
        success, error = valid_playlist(playlist, movie_id)
        if error ==  "Movie already exists in Playlist":
          already_exists_playlist.append(playlist.name)
    if len(already_exists_playlist) > 0:
      return render_template('playlist/add.html', playlists=playlists, movie_name=movie_name,
                                                          error=f"Movies already exists in Playlist {already_exists_playlist}")
        
    for playlist in playlists:
      # print(len(request.form.getlist(playlist.name)))
      success = None
      error = None     
      if len(request.form.getlist(playlist.name)) > 0:
        success, error = insert_Movie_to_playlist(playlist, movie_id)
        print("SUCESS: ", success)
        print("ERROR: ", error)
        if error ==  "Movie already exists in Playlist":
          error = f"Movie already exists in Playlist '{playlist.name}'"
          return render_template('playlist/add.html', playlists=playlists, movie_name=movie_name,error=error)
    return redirect(url_for('search.home'))
 
  return render_template('playlist/add.html', playlists=playlists, movie_name=movie_name)
 