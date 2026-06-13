
<div>
  <img src="https://img.shields.io/github/last-commit/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/code-size/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/top/nahuelmol/data.analysis"/>
  <img src="https://img.shields.io/github/languages/count/nahuelmol/data.analysis"/>
</div>

## About the project

This backend will receive .seg files
and process them by using different. Python is chosen for the implementation, taking advantage of its capabilities in data analysis.

Beyond seismic files, spreadsheet files (.csv .tsv .xlsx) will be also studied by applying data analysis techniques.

## Specialized libraries

Well known data analysis tools will be used on the backend, like:

*  numpy
*  pandas
*  scipy

In addition to Python's data analysis tools, specialized libraries are used to handle SEG files, for example:

*  segysak
*  segyio

Once a SEGY file arrives to the server, chart images are generated in .png format. The way to process it can be selected, mofifying the number of these images.

Being an APIrest based on json, png files must be converted to string files and finally be injected to the response json.

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

As an alternative to the above commad, a sever.py file can be used.

```
python serve.py
```

### Remote setting

Pushing by using access token:

```
git remote set-url origin https://TOKEN@github.com/OWNER/REPOSITORY.git
```

### Old versions

For older versions like mine, which is a windows 7 32 bits, older libraries are used. This is the case of Pandas, Numpy, Scipy, h5py, among others. These can be installed using the pip tool, indicating the specific version:

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


### Testing

Curl is used for sending multipart forms by reading a plain file, called upload.txt in this case, that has a modelo of an specific request:

```
curl -K tests/upload.txt
```

