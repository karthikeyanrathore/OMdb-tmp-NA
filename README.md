## OMdb-API (fasal work)

### set env variable
```
cat > .env
SECRET_KEY="" # openssl rand -base64 32
API_KEY="" # https://www.omdbapi.com/apikey.aspx
FLASK_ENV=developement
FLASK_DEBUG=1
```

### docker run
```
docker build -t fasal:latest .
docker run -it -d -p 5000:5000 fasal
goto "http://127.0.0.1:5000/auth/login"
```
## heroku docker deployment 
- https://fasal-docker.herokuapp.com/auth/login

