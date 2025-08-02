
from scipy.signal import freqz, butter, lfilter, firwin, ellip

class Filter:
    def __init__(self, filtertype):
        self.type = filtertype
        self.responseType = None
        self.setResponse()
        if(self.responseType == 'FIR'):
            self.coeffs = 0.0
        elif(self.responseType == 'IIR'):
            self.a = 0.0
            self.b = 0.0
        else:
            print('handle this')

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
        elif self.type in FIRfiters:
            self.responseType = 'FIR'
        else:
            print('not recognized type')
            return None

    def apply(self, signal):
        if(self.responseType == 'IIR'):
            return lfilter(self.b, self.a, signal)
        elif(self.responseType == 'FIR'):
            return filtfilt(self.coeff, signal)
        else:
            print('filter was not setted')






