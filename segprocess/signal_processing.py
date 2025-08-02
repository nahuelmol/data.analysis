import scipy
import base64
import xarray as xr
import numpy as np

from io import BytesIO
from scipy.signal import freqz, butter, firwin, ellip
from segysak.segy import segy_header_scan, segy_header_scrape, segy_bin_scrape
from segysak.segy import segy_loader

from segprocess.Filter import Filter

def applyFFilter(data, params, new_dataset):
    nyquist_f = 0.5 * params['sr']
    frec_norm = params['cut_freq'] / nyquist_f
    FILTER = Filter(params['filter_name']) 
    btype = params['filtertype']
    desired = params['gain']
    fs = params['fs']
    numtaps = params['numtaps']
    if(params['filter_name'] == 'butterworth'):
        coeffs = butter(params['order'], Wn=frec_norm, btype=btype, analog=False)
    elif (params['filter_name'] == 'cheby1'):
        coeffs = cheby1(params['order'], rs=40, Wn=frec_norm, btype=btype)
    elif (params['filter_name'] == 'cheby2'):
        coeffs = cheby2(params['order'], rs=40, Wn=frec_norm, btype=btype)
    elif (params['filter_name'] == 'elliptic'):
        coeffs = ellip(params['order'], rp=1, rs=40, Wn=frec_norm, btype=btype)
    elif (params['filter_name'] == 'bessel'):
        coeffs = bessel(params['order'], frec_norm, btype=btype, analog=False, nrom='phase')
    elif (params['filter_name'] == 'firwin'):
        coeffs = firwin(numtaps=numtaps, cutoff=cutoff, fs=fs, window=params['window'])
    elif (params['filter_name'] == 'firwin2'):
        coeffs = firwin2(numtaps=numtaps, cutoff=cutoff, fs=fs, window=params['window'])
    elif (params['filter_name'] == 'remez'):
        coeffs = remez(numtaps=numtaps, bands=bands, ftype=btype, desired=desired, fs=fs)
    elif (params['filter_name'] == 'firls'): 
        coeffs = firls(numtaps=numtaps, bands=bands, desired=desired, fs=fs)
    else:
        print('unrecognized filter')
        return False, None

    FILTER.setCoeff(coeffs)
    for i in range(ntrace):
        signal = data.isel(cdp=i)
        filtered = FILTER.apply(signal)
        new_dataset[dict(trace=i)] = filtered

    FILTER.plotFResponse()
    FILTER.plotTDResponse()
    FILTER.plotPoleZero()
    fresponse_str = FILTER.exportGraph('Fresponse')
    pole_zero_str = FILTER.exportGraph('poleZero')
    tdresponse_str= FILTER.exportGraph('TDresponse')

    REPORT = {
        'freq_response': fresponse_str,
        'image':new_dataset_str
    }
    return True, REPORT

def TraceSelector(selected_trace, sr, V3D):
    selected_trace = 0 #forcing
    air1 = V3D.isel(ILINE_3D=0, CROSSLINE_3D=0).data
    #para una misma imagen sismica (air1) puedo pintar cada traza
    signal = air1[selected_trace] #one trace selected
    plt.figure(figsize=(15, 8))
    nsamples = signal.size
    t_total = nsamples / sr #duracion de 3.004 segundos
    t = np.linspace(0, t_total, nsamples) #eje de tiempo
    plt.subplot(4, 1, 1)
    plt.plot(t, signal)
    plt.show()

def Details(signal):
    freq = np.fft.fftfreq(len(signal))
    spectra = np.fft.fft(signal)

    index = np.argmax(np.abs(spectra))
    dominant_f = freq[index]
    print("dominant frequency -> ", dominant_f)

    plt.figure(figsize=(15, 8))
    plt.plot(freq, np.abs(spectra))
    plt.title("Signal -> Fourier Transform")
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")

def segyProcess2d(data, params):
    print('data type: {}'.format(type(data)))
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
    res, report = applyFFilter(data, params)
    return res, report

def FFilter(file_str, params):
    bytes_file  = base64.b64decode(file_str)
    headers  = segy_header_scrape('temp_file.segy')
    dt = (headers['TRACE_SAMPLE_INTERVAL'].mean()) / 1000000
    sr = 1/dt
    params['sr'] = sr
    with open('temp_file.segy', 'wb') as f:
        f.write(bytes_file)
    loader = segy_loader('temp_file.segy')
    if(len(loader.data.dims) == 2):
        res, report = segyProcess2d(loader.data, params)
        return res, report
    elif (len(loader.data.dims) == 3):
        res, report = segyProcess3d(loader.data, params)
        return res, report
    else:
        print('unrecognized dimension')
        return False, None

def NMOFilter(file_str, params):
    pass
