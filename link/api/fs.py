import filetype
import base64
import tarfile
import segyio
import zipfile

import pandas as pd
import xarray as xr

from io import BytesIO

from link.api.grapher import do2dGraph
from link.api.data_analysis import PCAnalysis, ICAnalysis, Basics
from segprocess.signal_processing import FFilter, exploratory_analysis, NMOFilter
from segysak.segy import segy_header_scrape

class File:
    def __init__(self, file, metadata):
        self.name   = file.name
        self.size   = file.size
        self.bins   = file.read()
        self.extension = file.name.split(".")[-1]
        self.temp   = 'temp_file.{}'.format(self.extension)
        self.dt     = None
        self.sr     = None
        self.ny     = None

        self.segy   = False
        self.csv    = False
        self.tsv    = False
        self.zip    = False
        self.sep    = None

        #self.segy_params = ['anex','nmo', 'gain', 'fc', 'filtertype', 'filtername', 
        #                   'window', 'numtaps', 'order', 'convolve']
        self.available_stat_params = ['pca', 'ica', 'complete', 'basics', 'target', 'ncomps']

        self.params = {}
        self.report = {}
        
        self.nothing    = False


        for param in self.available_stat_params:
            if param in META:
                self.params[param] = META.get(param)

        #self.ffilter    = META.get('ffilter')
        #self.nmo        = META.get('nmo')
        #self.anex       = META.get('anex')
        #self.convolve   = META.get('convolve')

        #self.gain       = META.get('gain')
        #self.cut_freq   = META.get('fc')
        #self.filtertype = META.get('filtertype')
        #self.filtername = META.get('filtername')
        #self.window     = META.get('window')
        #self.numtaps    = META.get('numtaps')
        #self.order      = META.get('order')

        self.xdata  = META.get('xdata')
        self.ydata  = META.get('ydata')

    def write_temp(self):
        with open(self.temp, 'wb') as f:
            f.write(self.bins)

    def set_params(self, which):
        if which == 'stat':
            self.params['complete'] = self.complete
            self.params['basics'] = self.basics
            self.params['pca'] = self.pca
            self.params['ica'] = self.ica
            self.params['target'] = self.target
            self.params['ncomps'] = self.ncomps
        #elif which== 'segy':
        #    self.params['order']    = self.order
        #    self.params['numtaps']  = self.numtaps
        #    self.params['convolve'] = self.convolve
        #    self.params['ffilter']  = self.ffilter
        #    self.params['nmo']      = self.nmo
        #    self.params['anex']     = self.anex
        #    self.params['cut_freq'] = self.cut_freq
        #    self.params['window']   = self.window
        #    self.params['gain']     = self.gain
        #    self.params['filtertype']   = self.filtertype
        #    self.params['filtername']   = self.filtername
        #    self.params['segy_type']    = self.extension
        elif which == 'zip':
            print('params are all False or None, should I set them?')
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

    def file_type(self):
        kind = filetype.guess(self.bins)
        if kind is None:
            self.issegy()
            self.csv    = is_sv(self.bins, ',')
            self.tsv    = is_sv(self.bins, '\t')
            self.ssv    = is_sv(self.bins, ' ')
        elif kind.extension == 'zip':
            self.zip    = True
            self.csv    = False
            self.tsv    = False
            self.segy   = False
            self.ssv    = False
        else:
            self.zip    = False
            self.csv    = False
            self.tsv    = False
            self.segy   = False
            self.ssv    = False

    def read(self):
        self.file_type()
        if (self.csv == True or self.tsv == True or self.ssv == True):
            self.set_sep()
            self.set_params('stat')
            self.stat_reader()
        elif (self.segy == True):
            print('SEG files are not longer supported')
        #    self.set_params('segy')
        #    self.segy_reader()
        elif (self.zip == True):
            self.set_params('zip')
            self.zip_reader()
        else:
            self.params = {}
            self.report = {}
            print("unrecognized file")

    def stat_reader(self):
        bin_fl_object   = BytesIO(self.bins) #binary file-like object
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

    def segy_reader(self):
        headers  = segy_header_scrape(self.temp, silent=True)
        self.params['iline_3d'] = headers['INLINE_3D'] 
        self.params['xline_3d'] = headers['CROSSLINE_3D']
        self.params['dt'] = (headers['TRACE_SAMPLE_INTERVAL'].mean()) / 1000000
        self.params['sr'] = 1.0 / self.params['dt']
        self.params['ny'] = 0.5 * self.params['sr']

        if self.params['nmo'] == True:
            res, report = NMOfilter(self)
            self.report = report
        elif self.params['ffilter'] == True:
            res, report = FFilter(self)
            self.report = report
        elif self.params['anex'] == True:
            res, report = analysis_exploratory(self)
            self.report = report
        else:
            print('nothing to process')
            self.report = {}

    def dat_reader(self):
        #model builder
        bin_fl_object   = BytesIO(self.bins)
        data            = pd.read_csv(bin_fl_object, sep=self.sep, encoding='latin1')
        MODEL = ClassificationModel(data)
        MODEL.logistic_regression()
        self.report = MODEL.report
        print(self.report)

    def zip_reader(self):
        #unzip(self.temp)
        finaldestination = 'extracted'
        with zipfile.ZipFile(self.temp, 'r') as f:
            f.extractall(finaldestination)
            print('unziping completed')
        
        return True 
    
    def tar_reader(self):
        with tarfile.open(fileobject, 'r:*') as tar_ref:
            tar_ref.extractall(extract_to)

    def issegy(self):
        try:
            with segyio.open(self.temp, 'r', ignore_geometry=True) as f:
                self.segy = True
        except Exception as e:
            self.segy = False

def is_sv(bin_data, sep):
    text = bin_data.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    ncols = len(lines[0].split(sep))
    for line in lines:
        col = len(line.split(sep))
        if col != ncols:
            return False
    return True
