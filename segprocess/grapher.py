
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


