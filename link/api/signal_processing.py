import scipy
from scipy.signal import freqz, butter, lfilter, firwin

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

def FrecFilter(signal, sr):
    f_cut = 25
    butt_order = 15
    nyquist_freq = 0.5 * sr
    frec_norm = f_cut / nyquist_freq
    b, a = butter(butt_order, frec_norm, btype='low', analog=False)
    #aplying the filter
    filtered = lfilter(b,a, signal)




