import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FastICA
from sklearn.decomposition import PCA
from .plotmaker import Plotter
from .grapher import imageConverter
    
def PCAnalysis(data, params):
    target = data.pop(params['target'])
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            if col != params['target']:
                cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
    data.insert(0, params['target'], target)

    #data as features
    ncomps = params['ncomps']
    svd_solver = 'arpack'
    pcnames = []
    for i in range(ncomps):
        i += 1
        pcnames.append(f"PC{i}")

    pca = PCA(n_components=ncomps)
    pca.fit(data)
    pcs             = pca.transform(data) #principal components
    data_with_pcs   = pd.DataFrame(data=pcs,
                                columns=pcnames)
    complete = pd.concat([data_with_pcs, target], axis=1)
    variance = pca.explained_variance_ratio_
    lost_information = 1-np.sum(variance)

    REPORT = {
        'variance': variance,
        'file_str_pca_chart': ''
    }
    filepath = Plotter(complete, 'PCA - Principal Components Analysis')
    res, file_str = imageConverter(filepath)
    REPORT['file_str_pca_chart'] = file_str
    return res, REPORT

def ICAnalysis(data, params):
    #the same, select numerical columns (an what I aim to separate?)
    target = data.pop(params['target'])
    cols_to_drop = []
    for col in data.columns:
        if data[col].dtype != 'float64':
            if col != ref:
                cols_to_drop.append(col)
    data = data.loc[:, ~data.columns.isin(cols_to_drop)]
    data.insert(0, params['target'], target)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(data)

    ica     = FastICA(n_components=params['ncomps'], random_state=0)
    x_ica   = ica.fit_transform(x_scaled)
    ICs     = pd.DataFrame(x_ica, columns=['IC1', 'IC2'])
    result  = pd.concat([target, ICs], axis=1)
    REPORT  = {}
    res, file_str = imageConverter(filepath)
    REPORT['file_str_ica_chart'] = file_str
    return REPORT

def Basics(data, params):
    target = params['temperature']
    basics = {
            'mean': np.mean(target),
            'median':np.median(target),
            #we = #ask
            #np.average(target, weights=we)
            'var':np.var(target),
            'std':np.std(target),
            'min':np.min(target),
            'max':np.max(target),
            'ptp':np.ptp(target),
            'perc75':np.percentile(target, 75),
            'perc25':np.percentile(target, 25),
            'kurtosis':scipy.stats.kurtosis(target),
            'skew':scipy.stats.skew(target),
    }
    REPORT['basics'] = basics
    return REPORT

