import scipy
import base64
import xarray as xr
import numpy as np

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
    nyquist_f = 0.5 * params['sr']
    frec_norm = params['cut_freq'] / nyquist_f
    FILTER  = Filter(params['filtername']) 
    btype   = params['filtertype']
    desired = params['gain']
    fs = params['fs']
    numtaps = params['numtaps']
    if(params['filtername'] == 'butterworth'):
        coeffs = butter(params['order'], Wn=frec_norm, btype=btype, analog=False)
    elif (params['filtername'] == 'cheby1'):
        coeffs = cheby1(params['order'], rs=40, Wn=frec_norm, btype=btype)
    elif (params['filtername'] == 'cheby2'):
        coeffs = cheby2(params['order'], rs=40, Wn=frec_norm, btype=btype)
    elif (params['filtername'] == 'elliptic'):
        coeffs = ellip(params['order'], rp=1, rs=40, Wn=frec_norm, btype=btype)
    elif (params['filtername'] == 'bessel'):
        coeffs = bessel(params['order'], frec_norm, btype=btype, analog=False, nrom='phase')
    elif (params['filtername'] == 'firwin'):
        coeffs = firwin(numtaps=numtaps, cutoff=cutoff, fs=fs, window=params['window'])
    elif (params['filtername'] == 'firwin2'):
        coeffs = firwin2(numtaps=numtaps, cutoff=cutoff, fs=fs, window=params['window'])
    elif (params['filtername'] == 'remez'):
        coeffs = remez(numtaps=numtaps, bands=bands, ftype=btype, desired=desired, fs=fs)
    elif (params['filtername'] == 'firls'): 
        coeffs = firls(numtaps=numtaps, bands=bands, desired=desired, fs=fs)
    else:
        print('unrecognized filter')
        return False, None

    FILTER.setCoeff(coeffs)
    FILTER.setTargetDims(data)
    for i in range(FILTER.ntraces):
        signal = data.isel(cdp=i)
        filtered = FILTER.apply(signal)
        new_dataset[dict(trace=i)] = filtered

    FILTER.plotFResponse()
    FILTER.plotTDResponse()
    FILTER.plotPoleZero()
    fresponse_str = FILTER.exportGraph('Fresponse')
    pole_zero_str = FILTER.exportGraph('poleZero')
    tdresponse_str= FILTER.exportGraph('TDresponse')

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
    #res, report = applyFFilter(data, params)
    #return res, report
    return False, None

def FFilter(file, params):
    with open('temp_file.segy', 'wb') as f:
        f.write(file)
    loader  = segy_loader('temp_file.segy')
    header  = segy_header_scrape('temp_file.segy')
    dt = (header['TRACE_SAMPLE_INTERVAL'].mean()) / 1000000
    params['sr'] = 1/dt
    if(len(loader.data.dims) == 2):
        res, report = segyProcess2d(loader.data, params)
        return res, report
    elif(len(loader.data.dims) == 3):
        res, report = segyProcess3d(loader.data, params)
        return res, report
    else:
        print('unrecognized dimension')
        return False, None

def NMOFilter(file, params):
    pass
