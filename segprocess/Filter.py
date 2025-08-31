
import matplotlib.pyplot as plt
import numpy as np
import base64
import segyio

from scipy.signal import freqz, butter, lfilter, firwin, ellip
from segysak.segy import segy_writer

class Filter:
    def __init__(self, params):
        self.start = False
        self.ntraces = None 
        self.nsamples= None

        self.order  = params['order']
        self.type   = params['filtername']
        self.sr     = params['sr']
        self.nyq_f       = 0.5 * params['sr']
        self.cutoff      = params['cut_freq']
        self.Wn          = params['cut_freq'] / self.nyq_f
        self.btype       = params['filtertype']
        self.desired     = params['gain']
        self.fs          = params['fs']
        self.numtaps     = params['numtaps']

        self.IIRfilters = ['butterworth', 'cheby1', 'cheby2', 'elliptic', 'bessel']
        self.FIRfilters = ['firwin', 'firwin2', 'remez', 'firls']

        self.pathFResponse  = 'temp/{}_FResponse.png'.format(self.type)
        self.pathTDResponse = 'temp/{}_TDResponse.png'.format(self.type)
        self.pathPoleZero   = 'temp/{}_PoleZero.png'.format(self.type)

        self.pathSegyFile   = 'temp/{}_output_segy.segy'.format(self.type)
        self.pathSeismicImage = 'temp/{}_seismic_image.png'.format(self.type)
        self.pathOriginalImage = 'temp/original_seismic_image.png'

        self.responseType   = None
        self.setResponse()
        self.worN           = None
        if(self.responseType == 'FIR'):
            self.coeffs = 0.0
        elif(self.responseType == 'IIR'):
            self.a = 0.0
            self.b = 0.0
        else:
            print('handle this')

    def set_filter(self):
        if not(self.type in self.IIRfilters or self.type in self.FIRfilters):
            print('unrecognized filter')
            return False, None
        if(self.type == 'butterworth'):
            self.coeffs = butter(self.order, Wn=self.Wn, btype=self.btype, analog=False)
        elif (self.type == 'cheby1'):
            self.coeffs = cheby1(self.order, rs=40, Wn=self.Wn, btype=self.btype)
        elif (self.type == 'cheby2'):
            self.coeffs = cheby2(self.order, rs=40, Wn=self.Wn, btype=self.btype)
        elif (self.type == 'elliptic'):
            self.coeffs = ellip(self.order, rp=1, rs=40, Wn=self.Wn, btype=self.btype)
        elif (self.type == 'bessel'):
            self.coeffs = bessel(self.order, frec_norm, btype=self.btype, analog=False, nrom='phase')
        elif (self.type == 'firwin'):
            self.coeffs = firwin(numtaps=self.numtaps, cutoff=self.cutoff, fs=self.fs, window=self.window)
        elif (self.type == 'firwin2'):
            self.coeffs = firwin2(numtaps=self.numtaps, cutoff=self.cutoff, fs=fs, window=self.window)
        elif (self.type == 'remez'):
            self.coeffs = remez(numtaps=self.numtaps, bands=self.bands, btype=self.btype, desired=self.desired, fs=self.fs)
        elif (self.type == 'firls'): 
            self.coeffs = firls(numtaps=self.numtaps, bands=self.bands, desired=self.desired, fs=self.fs)
        else:
            print('GOING OUT')
            return False, None


    def set_target_dims(self, data):
        self.ntraces, self.nsamples = data.shape
        print('ntraces: {} - nsamples: {}'.format(self.ntraces, self.nsamples))

    def set_coeffs(self):
        if (isinstance(self.coeffs, tuple)):
            self.a = self.coeffs[0]
            self.b = self.coeffs[1]
        elif(isinstance(self.coeffs, list)):
            self.coeffs = self.coeffs
        else:
            print('not coefficients')

    def setResponse(self):
        if self.type in self.IIRfilters:
            self.responseType = 'IIR'
            self.worN = 8000
        elif self.type in self.FIRfiters:
            self.responseType = 'FIR'
            self.worN = 8000
        else:
            print('not recognized type')
            return None

    def apply(self, signal):
        if(self.start == False):
            print('unique')
            self.nsamples = len(signal)
            self.start = True
        if(self.responseType == 'IIR'):
            return lfilter(self.b, self.a, signal)
        elif(self.responseType == 'FIR'):
            return filtfilt(self.coeff, signal)
        else:
            print('filter was not setted')

    def exportGraph(self, which):
        filepath = ''
        if(which == 'Fresponse'):
            filepath = self.pathFResponse
        elif(which == 'TDresponse'):
            filepath = self.pathTDResponse
        elif(which == 'poleZero'):
            filepath = self.pathPoleZero
        else:
            print('not recognized target')
            return False, None
        with open(filepath, 'rb') as f:
            data = f.read()
            data_str = base64.b64encode(data).decode('utf-8')
        return True, data_str

    def plotTDResponse(self):
        h = None
        if(self.responseType == 'FIR'):
            h = self.coeffs
        elif(self.responseType== 'IIR'):
            impulse = np.zeros(self.nsamples)
            impulse[0] = 1
            h = lfilter(self.b, self.a, impulse)
        title = '{} - {}'.format(self.responseType, self.type)
        plt.stem(h, use_line_collection=True)
        plt.title(title)
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.grid()
        plt.savefig(self.pathTDResponse)

    def plotFResponse(self):
        w = None
        h = None
        if(self.responseType == 'IIR'):
            w, h = freqz(self.b, self.a, worN=self.worN)
        elif(self.responseType == 'FIR'):
            w, h = freqz(self.coeffs, [1], worN=self.worN)
        label = '{} filter'.format(self.type)
        title = 'Frequecy Response'
        plt.figure(figsize=(8,4))
        plt.plot(w /np.pi, 20 * np.log10(abs(h)), label=label)
        plt.title(title)
        plt.xlabel('Normalized Frequency')
        plt.ylabel('Magnitude (db)')
        plt.grid()
        plt.ylim(-60, 5)
        plt.legend()
        plt.savefig(self.pathFResponse)

    def plotPoleZero(self):
        zeros = None
        poles = None
        if(self.responseType == 'IIR'):
            zeros = np.roots(self.b)
            poles = np.roots(self.a)
        elif(self.responseType == 'FIR'):
            zeros = np.roots(self.coeffs)
            poles = np.roots([1])
        else:
            print('not response type setted\ncheck it!')
            return

        plt.figure(figsize=(6,6))
        plt.scatter(np.real(zeros), np.imag(zeros), marker='o', 
                    facecolors='none', edgecolors='blue', label='Poles')
        unit_circle = plt.Circle((0,0), 1, color='black', fill=False, linestyle='dashed')
        plt.gca().add_artist(unit_circle)
        plt.axhline(0, color='gray', linewidth=0.5)
        plt.axvline(0, color='gray', linewidth=0.5)
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.title('Pole-Zero Plot')
        plt.savefig(self.pathPoleZero)

    def write_segy(self, data):
        n_traces, n_samples = data.shape
        dt = data.attrs.get("dt", 4000)

        spec = segyio.spec()
        spec.sorting = 2
        spec.format = 5
        spec.samples = range(n_samples)
        spec.ilines = range(n_traces)
        spec.xlines = [1]

        with segyio.create(self.pathSegyFile, spec) as f:
            f.bin[segyio.BinField.Interval] = dt
            for i in range(n_traces):
                f.trace[i] = data[i,:].values.astype("float32")

    def plotSegy(self, data, which):
        n_traces, n_samples = data.shape
        dt = data.attrs.get("dt", 4000)
        title  = ''
        filename = ''
        if (which == 'original'):
            filename = self.pathOriginalImage
            title = 'Original Seismic Image'
        elif (which == 'processed'):
            filename = self.pathSeismicImage
            title = 'Processed Seismic Image'
        else:
            opc = input('not recognized which image; original(1) or processed(2)')
            if opc == 1:
                filename = 'original'
            elif opc == 2:
                filaname = 'processed'
            else: 
                return False, 'invalid option'

        arr = data.values
        t = np.arange(n_samples) * dt * 1e-6
        plt.figure(figsize=(12,6))
        plt.imshow(
                arr.T,
                aspect='auto',
                cmap='seismic',
                extent=[0, n_traces, t[-1], t[0]]
        )
        plt.xlabel("Trace")
        plt.ylabel("Time [s]")
        plt.title(title)
        plt.colorbar(label="Amplitude")
        plt.savefig(filename, dpi=300)
        return True, 'plot done!'

    def plot_filter_alone(self):
        if self.responseType == 'IIR':
            freq, resp = freqz(self.a, self.b)
            plt.plot(freq * self.sr /(2 * np.pi), 20 * np.log10(np.abs(resp)))
            plt.xlabel("Frequency")
            plt.ylabel("Amplitude")
            plt.savefig("here.png", dpi=300)

