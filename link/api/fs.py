import pandas as pd
import segysak
import xarray as xr
import filetype
import base64

#fileobject is the file-like object

def filetype(file_str, form):
    decode = base64.b64decode(file_str)
    kind = filetype.guess(decoded)
    myformat = ''
    if kind:
        myformat = kind.extension
    if(myformat == form):
        return True
    else:
        return False

def CSVreader(fileobject):
    df = pd.read_csv(fileobjetc, sep=';', encoding='utf-8')
    ndf = replace_na(df, 'mean')

def SEGYreader(fileobject, demand):
    from segysak.segy import segy_header_scan
    from segysak.segy import segy_loader
    
    V3D = xr.open_dataset(
        fileobject,
        #V3D_path,
        dim_byte_fields={"ILINE_3D":189, "CROSSLINE_3D":193, "ShotPoint":197 },
        extra_byte_fields={"CDP_X":181, "CDP_Y":185 },
    )
    #convolve_traces(V3D)
    #graph_traces(V3D)
    
    if demand == 'raw':
        image = graph_image(V3D)
        return image
    elif demand == 'freqfilter':
        return image
    elif demand == 'nmofilter':
        return iamge
    else:
        print('nothing to process')

def DATreader(fileobject):
    pass
def ZIPreader(fileobject):
    import zipfile
    with zipfile.ZipFile(fileobject, 'r') as zip_ref:
        zip_ref.extract()
    
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

def ValidateFile(file):
    if file == None:
        return False, 'None file'
    elif file == '':
        return False, 'empty string'
    elif type(file) != 'str':
        return False, 'wrong file type'
    elif type(file) == 'str':
        base64_file = file.encode('utf-8')
        if isvalid_base64(base64_file):
            return True, 'valid base64 file'
        else:
            return False, 'the file is not a valid base64'
    else:
        return False, 'something went wrong'


def FileReader(file_str):
    res, msg = ValidateFile(file_str)
    if res == False:
        return msg, False 
    if filetype(file_str, 'csv'):
        return CSVreader(file_str), True
    elif filetype(file_str, 'dat'):
        return DATreader(file_str), True
    elif filetype(file_str, 'segy'):
        return SEGYreader(file_str), True
    elif filetype(file_str, 'zip'):
        return ZIPreader(file_str), True
    elif filetype(file_str, 'tar'):
        return TARreader(file_str), True
    else:
        print("Filetype not recognized")
        return None, False

