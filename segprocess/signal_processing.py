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

def FFilter(file, params, extension):
    print('\n{}\n'.format(extension))
    temp_file = 'temp_file.{}'.format(extension)
    with open(temp_file, 'wb') as f:
        f.write(file)
    headers  = segy_header_scrape(temp_file, silent=True)
    dt = (headers['TRACE_SAMPLE_INTERVAL'].mean()) / 1000000
    params['sr'] = 1/dt
    n_inlines   = headers["INLINE_3D"].nunique() 
    n_xlines = headers["CROSSLINE_3D"].nunique() 
    if n_inlines == 1 and n_xlines == 1:
        loader  = segy_loader(temp_file)
        res, report = segyProcess2d(loader.data, params)
        return res, report
    else:
        print("thinkin on 3d")
        #res, report = segyProcess3d(data, params)
    return False, {}
    """
    if(len(loader.data.dims) == 2):
    elif(len(loader.data.dims) == 3):
        res, report = segyProcess3d(loader.data, params)
        return res, report
    else:
        print('unrecognized dimension')
        return False, None
    """

def NMOFilter(file, params):
    pass
