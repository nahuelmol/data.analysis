import scipy
import base64

from io import BytesIO
from scipy.signal import freqz, butter, lfilter, firwin
from segysak.segy import segy_header_scan, segy_header_scrape, segy_bin_scrape
from segysak.segy import segy_loader

def TraceGrapher(signal, filtered):
    plt.plot(t, air1[0])
    plt.plot(t, filtered)
    plt.show()

def SpecGrapher(signal, filtered):
    plt.magnitude_spectrum(filtered, scale='dB', label="Señal con filtro pasa bajo Butterworth")
    plt.magnitude_spectrum(signal, scale='dB', label="Señal sin filtro")
    plt.xlabel('Normalized frequency')
    plt.ylabel('Amplitude (dB)')
    plt.legend()
    plt.show();

def TraceSelector(selected_trace, sr, V3D):
    selected_trace = 0 #forcing
    air1 = V3D.isel(ILINE_3D=0, CROSSLINE_3D=0).data
    #para una misma imagen sismica (air1) puedo pintar cada traza
    signal = air1[selected_trace] #one trace selected
    plt.figure(figsize=(15, 8))
    nsamples = signal.size
    t_total = nsamples / sr #duracion de 3.004 segundos
    print("duration -> ", t_total)
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
    plt.show()

def segyProcess2d(data, params):
    filterType  = params['filtertype']
    filtername  = params['filter_name']
    cut_freq    = params['cut_freq']
    print(type(data))

def segyProcess3d(data, params):
    filterType  = params['filtertype']
    filtername  = params['filter_name']
    cut_freq    = params['cut_freq']
    order       = ''
    print(type(data))

    data = xr.open_dataset(
        bin_fl_object,
        dim_byte_fields={"ILINE_3D":189, "CROSSLINE_3D":193, "ShotPoint":197 },
        extra_byte_fields={"CDP_X":181, "CDP_Y":185 },
    )
    ntrace, nsamples = data.shape
    trace_name, sample_name = data.dims #hipotetic names
    new_dataset = xr.DataArray( np.zeros((n,m)),
                                dims=['trace', 'time'],
                                coords={'trace':np.arange(n),
                                   'time':np.arange(m)}
                                )

    nyquist_freq = 0.5 * params['sr']
    frec_norm = params['cut_freq'] / nyquist_freq
    if(filtertype == 'butterworth'):
        b, a = butter(params['butt_order'], frec_norm, btype='low', analog=False)
    else:
        print('unrecognized filter')
        return False, None

    for i in range(ntrace):
        signal = data.isel(trace_name=i)
        filtered = lfilter(b,a, signal)
        new_dataset.isel(trace=filtered)
    return True, new_dataset

def FFilter(file_str, params):
    bytes_file  = base64.b64decode(file_str)
    headers  = segy_header_scrape('temp_file.segy')
    for col in headers.columns:
        print("col: ", col)
    dt = headers['TRACE_SAMPLE_INTERVAL'].mean()
    sr = 1000/dt
    params['sr'] = sr
    with open('temp_file.segy', 'wb') as f:
        f.write(bytes_file)
    loader = segy_loader('temp_file.segy')
    if(len(loader.data.dims) == 2):
        res, image = segyProcess2d(loader.data, params)
        return res, image
    elif (len(loader.data.dims) == 3):
        res, image = segyProcess3d(loader.data, params)
        return res, image
    else:
        print('unrecognized dimension')
        return False, None
    REPORT = {}
    return False, REPORT


def NMOFilter(V3D):
    pass
