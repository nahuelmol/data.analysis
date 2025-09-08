import scipy
import base64
import xarray as xr
import numpy as np
import segyio

from io import BytesIO
from segysak.segy import segy_loader

from segprocess.Filter import Filter
from segprocess.seganex import Seganex

def convert_ascci(data):
    #waves = data.tobytes()
    #waves_b64 = base64.b64encode(waves).decode('utf-8')
    return str(data)
    
def applyFFilter(data, params, new_dataset):
    FILTER = Filter(params) 
    FILTER.set_filter()
    FILTER.set_coeffs()
    FILTER.set_target_dims(data)
    
    for i in range(FILTER.ntraces):
        signal = data.isel({data.dims[0]:i})
        filtered = FILTER.apply(signal)
        new_dataset[dict(trace=i)] = filtered

    FILTER.plot_filter_alone()
    FILTER.plotFResponse()
    FILTER.plotTDResponse()
    FILTER.plotPoleZero()

    FILTER.plotSegy(data, 'original')
    FILTER.write_segy(new_dataset)
    FILTER.plotSegy(new_dataset, 'processed')

    res, fresponse_str  = FILTER.exportGraph('Fresponse')
    res, pole_zero_str  = FILTER.exportGraph('poleZero')
    res, tdresponse_str = FILTER.exportGraph('TDresponse')
    res, origi_png_str  = FILTER.exportGraph('original')
    res, image_png_str  = FILTER.exportGraph('processed')

    new_dataset_str = convert_ascci(new_dataset)
    REPORT = {
        'freq_response': fresponse_str,
        'tdresponse':tdresponse_str,
        'pole_zero':pole_zero_str,
        'original':origi_png_str,
        'image':image_png_str
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
    nil     = file.params["iline_3d"].nunique() 
    nxl     = file.params["xline_3d"].nunique() 
    if nil == 1 and nxl == 1:
        loader  = segy_loader(file.temp)
        res, report = segyProcess2d(loader.data, file.params)
        return res, report
    else:
        print("thinkin on 3d")
        #res, report = segyProcess3d(data, params)
    return False, {}

def NMOFilter(file):
    pass

def analysis_exploratory(file):
    ANEX = Seganex(file.temp) 

    ANEX.metrics()
    ANEX.plot_spec()
    ANEX.export('spec')

    return True, ANEX.report
