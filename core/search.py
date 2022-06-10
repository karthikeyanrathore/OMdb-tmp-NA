from flask import Blueprint, g, request, render_template
from flask import session
from flask import Flask, redirect,url_for
import logging


from core.db import db
from core.auth import login_required
from core.ombd import get_movie

logger = logging.getLogger(f"SEARCH_HOME .{__name__}")
search_bp = Blueprint('search', __name__)

@search_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
  # search bar . 
  # make `/get` request to OMDb API.
  # return list.
  # each item (add_to_playlist)
  # if empty . create playlist
  # print(g.user)
  error = None
  if request.method == 'POST':
    movie_name = request.form['movie_name']
    
    if movie_name is None:
      error = "Movie Name is Required"
    
    # `/get` by id: https://www.omdbapi.com/?i={{movie_id}}&apikey={{api_key}}
    # `/get` by name: https://www.omdbapi.com/?s={{movie_name}}&apikey={{api_key}}
    
    # return list of movies (ex: batman)
    # # get info for each movie
    if error is None:
      movies, error = get_movie(movie=movie_name, apply_filter='NAME')
      if movies is None:
        return "ok"
      # print(movies)
      if error:
        # print('error: ', error)
        return render_template('search/home.html', error=error)
      # print(movies)
      # return 'working'
      if len(movies) > 0:
        return render_template('search/home.html', movies=movies)
    
  return render_template('search/home.html', error=error)

