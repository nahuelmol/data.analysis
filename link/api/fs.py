import segysak
import filetype
import base64
import tarfile
import segyio

import pandas as pd
import xarray as xr

from io import BytesIO

from link.api.grapher import do2dGraph
from link.api.data_analysis import PCAnalysis, ICAnalysis, Basics
from segprocess.signal_processing import FFilter

class File:
    def __init__(self, file, data):
        self.file   = file
        self.segy   = False
        self.csv    = False
        self.tsv    = False
        self.name   = None
        self.sep    = None

        self.segy_params = ['nmo', 'gain', 'fs', 'fc', 'filtype', 'filtname', 
                            'window', 'numtaps', 'order', 'convolve']
        self.stat_params = ['pca', 'ica', 'complete', 'basics', 'target', 'ncomps']

        self.params = {}
        self.report = {}
        
        self.file_format = data.get()
        self.basics = data.get('basics')
        self.complete = data.get('complete')
        self.pca = data.get('pca')
        self.ica = data.get('ica')
        self.nothing = False

        self.ffilter    = data.get('ffilter')
        self.nmo        = data.get('nmo')
        self.convolve   = data.get('convolve')

        self.gain       = data.get('gain')
        self.fs         = data.get('fs')
        self.cut_freq   = data.get('fc')
        self.filtertype = data.get('filtype')
        self.filtername = data.get('filtname')
        self.window     = data.get('window')
        self.numtaps    = data.get('numtaps')
        self.order      = data.get('order')

        self.xdata = data.get('xdata')
        self.ydata = data.get('ydata')

        self.target = data.get('target')
        self.ncomps = data.get('ncomps')

    def set_params(self, which):
        if which == 'stat':
            self.params['complete'] = self.complete
            self.params['basics'] = self.basics
            self.params['pca'] = self.pca
            self.params['ica'] = self.ica
            self.params['target'] = self.target
            self.params['ncomps'] = self.ncomps
        elif which== 'segy':
            self.params['order']    = self.order
            self.params['numtaps']  = self.numtaps
            self.params['convolve'] = self.convolve
            self.params['ffilter']  = self.ffilter
            self.params['nmo']      = self.nmo
            self.params['cut_freq'] = self.cut_freq
            self.params['window']   = self.window
            self.params['fs']   = self.fs
            self.params['gain'] = self.gain
            self.params['filtertype']   = self.filtertype
            self.params['filtername']   = self.filtername
        elif which == 'zip':
            print('idk')
        else:
            print('not found file type')

    def set_sep(self):
        if self.csv == True:
            self.sep = ","
        elif self.tsv == True:
            self.sep = "\t"
        elif self.ssv == True:
            self.sep = " "
        else:
            print('not separator')


    def file_type(self, form):
        kind = filetype.guess(self.file)
        myformat = ''
        if kind is None:
            self.segy   = issegy(self.file)
            self.csv    = is_sv(self.file, ',')
            self.tsv    = is_sv(self.file, '\t')
            self.ssv    = is_sv(self.file, ' ')
        else:
            self.csv = False
            self.tsv = False
            self.segy = False
            self.ssv = False

    def read_file(self):
        #take_extension()
        self.file_type()
        self.set_sep()
        if (self.csv == True or self.tsv == True or self.ssv == True):
            self.set_params('stat')
            res, report = self.stat_reader()
            self.report = report
        elif (self.segy == True):
            self.set_params('segy')
            res, report = self.segy_reader()
            self.report = report
        else:
            self.params = {}
            self.report = {}

    def stat_reader(self):
        bin_fl_object   = BytesIO(self.file) #binary file-like object
        data            = pd.read_csv(bin_fl_object, sep=self.sep, encoding='latin1')
        report = {}
        if self.complete == True:
            res, image = do2dGraph(data, self.params)
            report['2dgraph'] = image
            res, image = PCAnalysis(data, self.params)
            report['pca_report'] = image
            res, image = ICAnalysis(data, self.params)
            report['ica_report'] = image
            res, image = Basics(data, self.params)
            report['basics_report'] = image
            self.report = report
        elif self.nothing == True:
            res, cnt = do2dGraph(data, self.params)
            report['2dgraph'] = cnt
            self.report = report
        elif self.basics == True:
            res, basics_report = Basics(data, self.params)
            report['basics_report'] = basics_report
            res, image = do2dGraph(data, self.params)
            report['2dgraph'] = image
            self.report = report
        elif self.pca == True:
            res, cnt = do2dGraph(data, self.params)
            report['2dgraph'] = cnt
            res, cnt = PCAnalysis(data, self.params)
            report['pca_report'] = cnt
            self.report = report
        elif self.ica == True:
            res, cnt = do2dGraph(data, self.params)
            report['2dgraph'] = cnt
            res, cnt = ICAnalysis(data, self.params)
            report['ica_report'] = cnt
            self.report = report
        else:
            self.report = {}

    def segy_reader(self.file):
        if params['process']:
            if self.nmo == True:
                res, report = NMOfilter(self.file, self.params)
                self.report = report
            elif self.ffilter == True:
                res, report = FFilter(self.file, self.params)
                self.report = report
            else:
                print('nothing to process')
                self.report = report

    def dat_reader(self):
        pass
    def zip_reader(self):
        #unzip(file_str)
        #return True 
        pass    
    
    def tar_reader(self):
        with tarfile.open(fileobject, 'r:*') as tar_ref:
            tar_ref.extractall(extract_to)

def isvalid_base64(s):
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False


def issegy(bin_data):
    try:
        with open('temp.segy', 'wb') as f:
            f.write(bin_data)
        with segyio.open('temp.segy', 'r', ignore_geometry=True) as f:
            return True
    except Exception as e:
        return False

def is_sv(bin_data, sep):
    text = bin_data.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    ncols = len(lines[0].split(sep))
    for line in lines:
        col = len(line.split(sep))
        if col != ncols:
            return False
    return True
