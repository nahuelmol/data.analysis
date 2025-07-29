import pandas as pd
import segysak
import xarray as xr
import filetype
import base64
from io import BytesIO

import segyio
from link.api.grapher import do2dGraph
from link.api.data_analysis import PCAnalysis, ICAnalysis, Basics

def issegy(bin_data):
    try:
        with open('temp.segy', 'wb') as f:
            f.write(bin_data)
        with segyio.open('temp.segy', 'r', ignore_geometry=True) as f:
            return True
    except Exception as e:
        return False
def iscsv(bin_data):
    text = bin_data.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    sep = ","
    ncols = len(lines[0].split(sep))
    for line in lines:
        col = len(line.split(sep))
        if col != ncols:
            return False
    return True

def FileType(file_str, form):
    #form is not being used
    bin_data = base64.b64decode(file_str)
    kind = filetype.guess(bin_data)
    myformat = ''
    if kind is None:
        #not recognized type
        #plain text for csv dat
        res_seg = issegy(bin_data)
        if res_seg:
            return True
        res_csv = iscsv(bin_data)
        if res_csv:
            return True
        return False
    else:
        if(kind.extension == form):
            return True
        else:
            return False

def CSVreader(file_str, params):
    bytes_file      = base64.b64decode(file_str)
    bin_fl_object   = BytesIO(bytes_file) #binary file-like object
    data            = pd.read_csv(bin_fl_object, sep=',', encoding='latin1')
    report = {}
    if params['process'] == 'complete':
        report['2dgraph'] = do2dGraph(data, params)
        report['pca_report'] = PCAnalysis(data, params)
        report['ica_report'] = ICAnalysis(data, params)
        report['basics_report'] = Basics(data, params)
        return True, report
    elif params['process'] == 'nothing':
        report['2dgraph'] = do2dGraph(data, params)
        return True, report
    elif params['process'] == 'basics':
        report['basics_report'] = Basics(data, params)
        report['2dgraph'] = do2dGraph(data, params)
        #define target
        return True, report
    elif params['process'] == 'pca':
        report['2dgraph'] = do2dGraph(data, params)
        report['pca_report'] = PCAnalysis(data, params)
        return True, report
    else:
        return False, None

def SEGYreader(file_str, demand):
    from segysak.segy import segy_header_scan
    from segysak.segy import segy_loader

    bytes_file = base64.b64encode(file_str)
    bin_fl_object = BytesIO(bytes_file) #binary file-like object
    header = segy_header_scan(bin_fl_object)
    dt = header.loc["TRACE_SAMPLE_EXAMPLE"]["mean"]
    sr = 1000/dt
    
    V3D = xr.open_dataset(
        bin_fl_object,
        dim_byte_fields={"ILINE_3D":189, "CROSSLINE_3D":193, "ShotPoint":197 },
        extra_byte_fields={"CDP_X":181, "CDP_Y":185 },
    )
    #convolve_traces(V3D)
    #graph_traces(V3D)
    
    if demand == 'raw':
        #image = graph_image(V3D)
        #return image
        pass
    elif demand == 'freqfilter':
        #image = FreqFilter(V3D, sr)
        #return image
        pass
    elif demand == 'nmofilter':
        #image = NMOFilter(V3D, sr)
        #return image
        pass
    else:
        print('nothing to process')

def DATreader(file_str):
    pass
def ZIPreader(file_str):
    unzip(file_str)
    
def TARreader(fileobject):
    import tarfile
    with tarfile.open(fileobject, 'r:*') as tar_ref:
        #'r:*' mode that detects the compression (gz, bz2, etc)
        tar_ref.extractall(extract_to)

def isvalid_base64(s):
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False

def ValidateFile(file_str):
    if file_str == None:
        return False, 'None file'
    elif file_str == '':
        return False, 'empty string'
    elif not isinstance(file_str, str):
        return False, 'wrong file type'
    elif isinstance(file_str, str):
        base64_file = file_str.encode('utf-8')
        if isvalid_base64(base64_file):
            return True, 'valid base64 file'
        else:
            return False,'the file is not a valid base64'
    else:
        return False, 'something went wrong'


def FileReader(file_str, params):
    res, msg = ValidateFile(file_str) #is or not a file
    if res == False:
        return False, msg

    if FileType(file_str, 'csv'):
        res, report = CSVreader(file_str, params), True
        return True, report
    elif FileType(file_str, 'dat'):
        res, report = DATreader(file_str, params), True
        return True, report
    elif FileType(file_str, 'segy'):
        res, report = SEGYreader(file_str, params)
        if res:
            return True, report
        else:
            return False, 'no possible'
    elif FileType(file_str, 'zip'):
        res, report = ZIPread(file_str)
        return True, report
    elif FileType(file_str, 'tar'):
        res, report = TARreader(file_str)
        return True, report
    else:
        return False, 'Filetype not recognized' 

