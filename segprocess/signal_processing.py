import scipy
import base64
import xarray as xr
import numpy as np
import segyio

from io import BytesIO
from scipy.signal import freqz, butter, firwin, ellip
from segysak.segy import segy_header_scan, segy_header_scrape, segy_bin_scrape
from segysak.segy import segy_loader

from segprocess.Filter import Filter

def convert_ascci(data):
    #waves = data.tobytes()
    #waves_b64 = base64.b64encode(waves).decode('utf-8')
    return str(data)
    
def applyFFilter(data, params, new_dataset):
    FILTER  = Filter(params) 
    FILTER.set_filter()
    FILTER.set_coeffs()
    FILTER.set_target_dims(data)
    for i in range(FILTER.ntraces):
        signal = data.isel(cdp=i)
        filtered = FILTER.apply(signal)
        new_dataset[dict(trace=i)] = filtered

    FILTER.plot_filter_alone()
    FILTER.plotFResponse()
    FILTER.plotTDResponse()
    FILTER.plotPoleZero()

    FILTER.plotSegy(data, 'original')
    FILTER.write_segy(new_dataset)
    FILTER.plotSegy(new_dataset, 'processed')
    fresponse_str = FILTER.exportGraph('Fresponse')
    pole_zero_str = FILTER.exportGraph('poleZero')
    tdresponse_str= FILTER.exportGraph('TDresponse')
    #FILTER.exportGraph('seismic_image')

    new_dataset_str = convert_ascci(new_dataset)
    REPORT = {
        'freq_response': fresponse_str,
        'tdresponse':tdresponse_str,
        'pole_zero':pole_zero_str,
        'image':new_dataset_str,
    }
    return True, REPORT

def segyProcess2d(data, params):
    ntrace, nsamples = data.shape
    trace_name, sample_name = ('trace', 'sample')
    shape = (ntrace, nsamples)
    coords = {
        trace_name:np.arange(ntrace), 
        sample_name:np.arange(nsamples),
    }
    new_dataset = xr.DataArray( np.zeros(shape, dtype=float),
                                dims=[trace_name, sample_name],
                                coords=coords,
                                )
    res, report = applyFFilter(data, params, new_dataset)
    return res, report

def segyProcess3d(data, params):
    info = data.shape
    print(info)
    #res, report = applyFFilter(data, params) #return res, report return False, None

def FFilter(file):
    file_in_bytes   = file.file
    with open(self.temp, 'wb') as f:
        f.write(file_in_bytes)
    headers  = segy_header_scrape(temp, silent=True)
    dt = (headers['TRACE_SAMPLE_INTERVAL'].mean()) / 1000000
    file.params['sr'] = 1/dt
    n_inlines   = headers["INLINE_3D"].nunique() 
    n_xlines = headers["CROSSLINE_3D"].nunique() 
    if n_inlines == 1 and n_xlines == 1:
        loader  = segy_loader(temp)
        res, report = segyProcess2d(loader.data, file.params)
        return res, report
    else:
        print("thinkin on 3d")
        #res, report = segyProcess3d(data, params)
    return False, {}

def NMOFilter(file):
    pass

def analysis_exploratory(file):
    with segyio.open(file.temp, 'r', ignore_geometry=True) as f:
        dt = f.bin[segyio.BinField.Interval]
        trace = f.trace[0]
        N = len(trace)
        frequencies = np.fft.rfftfreq(N, d=dt)
        spectrum    = np.abs(np.fft.rfft(trace))
        dominant    = frequencies[np.argmax(spectrum)]

        REPORT = {
            'dominant_frequecy': dominant,
        }
        print(REPORT)
        return True, REPORT
    return False, {}
