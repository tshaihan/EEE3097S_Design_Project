import numpy as np
from scipy.signal import correlate, correlation_lags


def time_delays(signals, fs=1):
    cross_correlations = np.empty_like(signals[1:])
    lags = np.empty_like(signals[1:])
    delays = np.zeros(len(signals)-1)
    for i in range(len(signals)-1):
        cross_correlations[i] = correlate(signals[0], signals[i+1], mode='same')
        lags[i] = np.array(correlation_lags(len(signals[0]), len(signals[i+1]),  mode='same'), dtype='float') / fs
        delays[i] = lags[i][np.argmax(cross_correlations[i])]
    return delays, cross_correlations, lags
