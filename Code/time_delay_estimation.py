import numpy as np
from gcc_phat import gcc_phat


# Estimates the delays of the given signals with respect to the reference signal
def estimate_delays(signals, ref_signal, fs=1, max_delay=None, interpolation=16):
    # Converts signals to arrays
    signals = np.asarray(signals)
    ref_signal = np.asarray(ref_signal)

    # Creates arrays for results
    num_signals = len(signals)
    delays = np.empty(num_signals)
    cross_correlations = [[] for _ in range(num_signals)]
    lags = [[] for _ in range(num_signals)]

    # Estimates delays using GCC-PHAT
    for i in range(num_signals):
        delays[i], cross_correlations[i] = gcc_phat(signals[i], ref_signal, fs, max_delay, interpolation)
        cc_len = int(len(cross_correlations[i]) / (2 * interpolation))
        lags[i] = np.linspace(-cc_len, cc_len + 1, len(cross_correlations[i]))

    # Converts results to arrays
    cross_correlations = np.asarray(cross_correlations)
    lags = np.asarray(lags) / fs

    return delays, cross_correlations, lags
