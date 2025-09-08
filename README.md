
<div>
  <img src="https://img.shields.io/github/last-commit/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/code-size/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/top/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/count/nahuelmol/data.analysis"/>
</div>

## About the project

This backend will receive .seg files
and process them by using different. Python is chosen for the implementation, taking advantage of its capabilities in data analysis.

Beyond seismic files, spreadsheets (.csv .tsv .xlsx) will be also studied applying data analysis techniques to reveal hidden patterns not evident at first glance.

## Specialized libraries
In addition to Python's data analysis tools, specialized libraries are used to handle SEG files. Examples are:

*segysak

*segyio

Once a SEGY file arrives to the server, varied chart image are generated in .png format. The type of processing can be selected, then the number of those images vary. 

Being a APIrest based on json, png files must be converted to string files and finally be injected to the response json.

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

The development server is built for debugging and fast tests, not for production and supported on Windows buffers. However, when large files are uploaded, Django's server is unable to handle them properly because mentioned buffers get fill.

That's why waitress is used. This wsgi server is robust and estable for handling heavy files uploading, being able to process chunks more efficiently, avoiding the overuse of Windows buffers and preventing related issues.

As alternative to the above commad, a sever.py file can be used.

```
python serve.py
```

### Remote setting
Pushing with personal access token.

```
git remote set-url origin https://TOKEN@github.com/OWNER/REPOSITORY.git
```

### Old versions

For CPU older versions like windows 7 32 bits, older libraries were used. Thid is the case of Pandas, Numpy, Scipy, h5py, among others. Which can be installed with pip by indicating their specific version:

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


### testing

Curl is used for sending multipart forms through upload.txt typing:

```
curl -K tests/upload.txt
```

