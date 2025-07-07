
<div>
  <img src="https://img.shields.io/github/last-commit/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/code-size/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/top/nahuelmol/data.analysis"/>
    <img src="https://img.shields.io/github/languages/count/nahuelmol/data.analysis"/>
</div>

## About the project

This backend will receive .seg files
and process them by using different. Python is chosen for the implementation, taking advantage of its capabilities in data analysis.

## Specialized libraries
In addition to Python's data analysis tools, specialized libraries are used to handle SEG files. Examples are:

*segysak

*segyio

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

### Remote setting
Pushing with personal access token.

```
git remote set-url origin https://TOKEN@github.com/OWNER/REPOSITORY.git
```

### Old versions

For CPU older versions like windows 7 32 bits, older libraries were used. Thid is the cade of Pandas, Numpy, Scipy, h5py, among others. Which can be installed by typing:

```
pip install pandas==1.3.4
```

It's the same than downloading its wheel directly and typing:

```
pip install <example.whl>
```

Examples are:

* pandas-1.3.4-cp38-cp38-win32.whl
* numpy-1.21.4-cp38-cp38-win32.whl
* scipy-1.5.4-cp38-cp38-win32.whl

which are in
* https://pypi.org/project/pandas/1.3.4/#files
* https://pypi.org/project/numpy/1.21.4/#files
* https://pypi.org/project/scipy/1.5.4/#files
