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

### Old versions

For oldest versions like windows 7 32 bits, it's better to donwload wheel files of the specfic versions that our CPU can work with. Examples are:

* pandas-1.3.4-cp38-cp38-win32.whl
* numpy-1.21.4-cp38-cp38-win32.whl

which are in
* https://pypi.org/project/pandas/1.3.4/#files
* https://pypi.org/project/numpy/1.21.4/#files
