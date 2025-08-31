import filetype
import base64
import tarfile
import segyio

import pandas as pd
import xarray as xr

from io import BytesIO

from link.api.grapher import do2dGraph
from link.api.data_analysis import PCAnalysis, ICAnalysis, Basics
from segprocess.signal_processing import FFilter, analysis_exploratory, NMOFilter
from segysak.segy import segy_header_scrape

class File:
    def __init__(self, file, data):
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
        self.sep    = None

        self.segy_params = ['anex','nmo', 'gain', 'fc', 'filtertype', 'filtername', 
                            'window', 'numtaps', 'order', 'convolve']
        self.stat_params = ['pca', 'ica', 'complete', 'basics', 'target', 'ncomps']

        self.params = {}
        self.report = {}
        
        self.basics = data.get('basics')
        self.complete = data.get('complete')
        self.pca = data.get('pca')
        self.ica = data.get('ica')
        self.nothing = False

        self.ffilter    = data.get('ffilter')
        self.nmo        = data.get('nmo')
        self.anex       = data.get('anex')
        self.convolve   = data.get('convolve')

        self.gain       = data.get('gain')
        self.cut_freq   = data.get('fc')
        self.filtertype = data.get('filtertype')
        self.filtername = data.get('filtername')
        self.window     = data.get('window')
        self.numtaps    = data.get('numtaps')
        self.order      = data.get('order')

        self.xdata = data.get('xdata')
        self.ydata = data.get('ydata')

        self.target = data.get('target')
        self.ncomps = data.get('ncomps')

    def write_temp(self):
        with open(self.temp, 'wb') as f:
            f.write(self.bins)
        headers  = segy_header_scrape(self.temp, silent=True)
        self.params['dt'] = (headers['TRACE_SAMPLE_INTERVAL'].mean()) / 1000000
        self.params['sr'] = 1.0 / self.params['dt']
        self.params['ny'] = 0.5 * self.params['sr']
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
            self.params['anex']     = self.anex
            self.params['cut_freq'] = self.cut_freq
            self.params['window']   = self.window
            self.params['gain']     = self.gain
            self.params['filtertype']   = self.filtertype
            self.params['filtername']   = self.filtername
            self.params['segy_type']    = self.extension
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


    def file_type(self):
        kind = filetype.guess(self.bins)
        if kind is None:
            self.issegy()
            self.csv    = is_sv(self.bins, ',')
            self.tsv    = is_sv(self.bins, '\t')
            self.ssv    = is_sv(self.bins, ' ')
        else:
            self.csv = False
            self.tsv = False
            self.segy = False
            self.ssv = False

    def read_file(self):
        self.file_type()
        if (self.csv == True or self.tsv == True or self.ssv == True):
            self.set_sep()
            self.set_params('stat')
            self.stat_reader()
        elif (self.segy == True):
            self.set_params('segy')
            self.segy_reader()
        else:
            self.params = {}
            self.report = {}

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
        pass
    def zip_reader(self):
        #unzip(file_str)
        #return True 
        pass    
    
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
