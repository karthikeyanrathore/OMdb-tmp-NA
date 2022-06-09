# movie OMBD_API
# get by name https://www.omdbapi.com/?s={{movie_name}&apikey={{api_key}} return list
# get by id https://www.omdbapi.com/?i={{movie_id}&apikey={{api_key}} return val.

import requests

from core.config import API_KEY
'''
movie_info = {
'title': [],
'year': [],
'imdbID': None,
'type': None,
'poster_url': None,

}
'''


def get_by_name(movie):
  API = 'https://www.omdbapi.com/'
  params = (('s', movie), ('apikey', API_KEY))
  response = requests.get(API, params=params)  
  error = None
  
  if response.status_code == 200:
    # replace logger
    print('API is working')
  else:
    error = "API is not Working"
    # print(error)
  
  movies = []
  if error is None:
    data = response.json()
    if data['Response'] == 'False':
      error = data['Error']
      return movies, error
    # movie_info = {}
    for i in range (0, len(data['Search'])):
      movie_info = {}
      movie_info['title'] = data['Search'][i]['Title']
      movie_info['year'] = data['Search'][i]['Year']
      movie_info['imdbID'] = str(data['Search'][i]['imdbID'])
      movie_info['type'] = data['Search'][i]['Type']
      movie_info['poster_url'] = data['Search'][i]['Poster']
      # print(movie_info)
      movies.append(movie_info)
    print(movies)
    return movies, error
     
      

def get_movie(movie, apply_filter):
  # get by name
  if apply_filter == 'NAME':
    movies = get_by_name(movie)
    return movies
  
  # get by id
  elif apply_filter == 'ID':
    pass
  # invalid filter
  else:
    pass
