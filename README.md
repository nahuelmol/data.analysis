## Running the server

### Linux

Gunicorn is the most used option, ideal for robust applications

```
python -m gunicorn mybackend.asgi:application -k uvicorn.workers.UvicornWorker 
```

### Windows

This can be executed as a wsgi application.
In this case waitress is used. It is a python pure server, ideal for web applications built with Django.

```
waitress-serve --port=8000 mybackend.wsgi:application
```

### remote setting

```
git remote set-url origin https://TOKEN@github.com/OWNER/REPOSITORY.git
```
