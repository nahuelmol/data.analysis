
import matplotlib.pyplot as plt
import numpy as np
import segyio
import base64

from datetime import datetime
from scipy.signal import spectrogram

class Seganex:
    def __init__(self, temp):
        self.time = datetime.now()
        self.temp = temp
        self.path_spec = 'temp/spec.png'
        self.report = {}

    def plot_spec(self):
        with segyio.open(self.temp, 'r', ignore_geometry=True) as f:
            data = np.array([trace for trace in f.trace])
            dt  = segyio.dt(f)
            signal = data.flatten()
            f, t, Sxx = spectrogram(signal, fs=1/dt, nperseg=512)
            plt.figure(figsize=(12,6))
            plt.pcolormesh(t, f, 10 * np.log(Sxx), shading="gouraud")
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("Time [s]")
            plt.title("Spectrogram")
            plt.colorbar(label="dB")
            plt.savefig(self.path_spec, dpi=300)

    def metrics(self):
        with segyio.open(self.temp, 'r', ignore_geometry=True) as f:
            dt = f.bin[segyio.BinField.Interval]
            trace = f.trace[0]
            N = len(trace)
            frequencies = np.fft.rfftfreq(N, d=dt)
            spectrum    = np.abs(np.fft.rfft(trace))
            self.report['f_dom'] = frequencies[np.argmax(spectrum)]


    def export(self, which):
        path = ''
        if which == 'spec':
            path = self.path_spec
        with open(path, 'rb') as f:
            data = f.read()
            strr = base64.b64encode(data).decode('utf-8')
            self.report['spec'] = strr




