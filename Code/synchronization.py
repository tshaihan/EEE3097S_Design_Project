import numpy as np
from scipy.signal import correlate, correlation_lags


def shift(sig, shift, fs=1):
    shift = int(shift * fs)
    if shift >= 0:
        sig[shift:] = sig[:len(sig)-shift]
        sig[:shift] = 0
    else:
        shift = abs(shift)
        sig[:len(sig) - shift] = sig[shift:]
        sig[len(sig) - shift:] = 0
    return sig


def synchronize(signals, ref_signals, fs=1):
    cross_correlations = np.empty_like(ref_signals[1:])
    lags = np.empty_like(ref_signals[1:])
    delays = np.zeros(len(ref_signals)-1)
    for i in range(len(ref_signals)-1):
        cross_correlations[i] = correlate(ref_signals[0], ref_signals[i+1], mode='same')
        lags[i] = np.array(correlation_lags(len(ref_signals[0]), len(ref_signals[i+1]), mode='same'), dtype='float') / fs
        delays[i] = lags[i][np.argmax(cross_correlations[i])]
        signals[i+1] = shift(signals[i+1], delays[i], fs)

    return signals, delays, cross_correlations, lags
