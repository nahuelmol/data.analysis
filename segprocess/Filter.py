
from scipy.signal import freqz, butter, lfilter, firwin, ellip
import matplotlib.pyplot as plt
import numpy as np
import base64

class Filter:
    def __init__(self, filtername):
        self.start = False
        self.ntraces = None 
        self.nsamples= None
        self.type = filtername
        self.pathFResponse  = 'temp/{}_FResponse.png'.format(filtername)
        self.pathTDResponse = 'temp/{}_TDResponse.png'.format(filtername)
        self.pathPoleZero   = 'temp/{}_PoleZero.png'.format(filtername)
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

    def setTargetDims(self, data):
        self.ntraces, self.nsamples = data.shape
        print('ntraces: {} - nsamples: {}'.format(self.ntraces, self.nsamples))

    def setCoeff(self, coeffs):
        if (type(coeffs) == tuple):
            self.a = coeffs[0]
            self.b = coeffs[1]
        elif (type(coeffs) == list):
            self.coeffs = coeffs
        else:
            print('not coefficients')

    def setResponse(self):
        IIRfilters = ['butterworth', 'cheby1', 'cheby2', 'elliptic', 'bessel']
        FIRfilters = ['firwin', 'firwin2', 'remez', 'firls']
        if self.type in IIRfilters:
            self.responseType = 'IIR'
            self.worN = 8000
        elif self.type in FIRfiters:
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








