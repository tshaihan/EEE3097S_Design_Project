import numpy as np
from scipy.signal import correlate, correlation_lags


# Determines the TDoA values between the first signal and the remaining signals
def tdoa(src_signals, fs=1):
    src_signals = np.array(src_signals)
    cross_correlations = np.empty_like(src_signals[1:])
    lags = np.empty_like(src_signals[1:])
    delays = np.zeros(len(src_signals)-1)
    for i in range(len(src_signals)-1):
        cross_correlations[i] = correlate(src_signals[0], src_signals[i+1], mode='same')
        lags[i] = np.array(correlation_lags(len(src_signals[0]), len(src_signals[i+1]),  mode='same'), dtype='double') / fs
        delays[i] = lags[i][np.argmax(cross_correlations[i])]

    return delays, cross_correlations, lags
