import pandas as pd
import segysak
import xarray as xr
import filetype
import base64
from io import BytesIO

import segyio
from link.api.grapher import do2dGraph
from link.api.data_analysis import PCAnalysis, ICAnalysis, Basics
from segprocess.signal_processing import FFilter

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
    bin_data = base64.b64decode(file_str)
    kind = filetype.guess(bin_data)
    myformat = ''
    if kind is None:
        res_seg = issegy(bin_data)
        if res_seg:
            if (form == 'segy'):
                return True
        res_csv = iscsv(bin_data)
        if res_csv:
            if (form == 'csv'):
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
        res, image = do2dGraph(data, params)
        report['2dgraph'] = image
        res, image = PCAnalysis(data, params)
        report['pca_report'] = image
        res, image = ICAnalysis(data, params)
        report['ica_report'] = image
        res, image = Basics(data, params)
        report['basics_report'] = image
        return True, report
    elif params['process'] == 'nothing':
        res, cnt = do2dGraph(data, params)
        report['2dgraph'] = cnt
        return True, report
    elif params['process'] == 'basics':
        res, basics_report = Basics(data, params)
        report['basics_report'] = basics_report
        res, image = do2dGraph(data, params)
        report['2dgraph'] = image
        return True, report
    elif params['process'] == 'pca':
        res, cnt = do2dGraph(data, params)
        report['2dgraph'] = cnt
        res, cnt = PCAnalysis(data, params)
        report['pca_report'] = cnt
        return True, report
    elif params['process'] == 'ica':
        res, cnt = do2dGraph(data, params)
        report['2dgraph'] = cnt
        res, cnt = ICAnalysis(data, params)
        report['ica_report'] = cnt
        return True, report
    else:
        return False, None

def SEGYreader(file_str, params):
    if params['process']:
        if params['process'] == 'nmo':
            res, report = NMOfilter(filter_str, params)
            return res, report
        elif params['process'] == 'ffilter':
            res, report = FFilter(file_str, params)
            return res, report
        else:
            print('nothing to process')
            return False, None

def DATreader(file_str, params):
    pass
def ZIPreader(file_str, params):
    unzip(file_str)
    return True 
    
def TARreader(fileobject):
    import tarfile
    with tarfile.open(fileobject, 'r:*') as tar_ref:
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
        res, report = CSVreader(file_str, params)
        if res:
            return True, report
        else:
            return False, None
    elif FileType(file_str, 'dat'):
        res, report = DATreader(file_str, params), True
        return True, report
    elif FileType(file_str, 'segy'):
        res, report = SEGYreader(file_str, params)
        if res:
            return True, report
        else:
            return False, None 
    elif FileType(file_str, 'zip'):
        res, report = ZIPread(file_str)
        return True, report
    elif FileType(file_str, 'tar'):
        res, report = TARreader(file_str)
        return True, report
    else:
        return False, 'Filetype not recognized' 

