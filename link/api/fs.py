import pandas as pd
import segysak
import xarray as xr

#fileobject is the file-like object

def filetype(filename, form):
    ending = ''
    for each in filename[::-1]:
        ending.push(each)
        if each == '.':
            break
    myformat = ending[::-1]
    if(myformat == form):
        return true
    else:
        return false

def CSVreader(fileobject):
    df = pd.read_csv(fileobjetc, sep=';', encoding='utf-8')
    #data cleaning
    ndf = replace_na(df, 'mean')
    #print(df.info())
    #print(df.head())
    #print(df.describe())

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

def FileReader(fileobject):
    filename = fileobject.filename
    if filetype(filename, 'csv'):
        return CSVreader(fileobject), True
    elif filetype(filename, 'dat'):
        return DATreader(fileobject), True
    elif filetype(filename, 'segy'):
        return SEGYreader(fileobject), True
    elif filetype(filename, 'zip'):
        return ZIPreader(fileobject), True
    elif filetype(filename, 'tar'):
        return TARreader(fileobject), True
    else:
        print("filetype is not recognized")
        return None, False

