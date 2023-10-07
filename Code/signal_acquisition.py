import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt


def process_signals(signals, fs, fc_low, fc_high, filter_order, clip_size):
    # Applies processing to each signal
    for i in range(len(signals)):
        # Applies bandpass filter
        sos = butter(filter_order, [fc_low, fc_high], btype='bandpass', output='sos', fs=fs)
        signals[i] = sosfilt(sos, signals[i])
        # Removes beginning portions of signals
        signals[i][:int(clip_size * fs)] = 0
        # Normalizes signals
        signals[i] = np.divide(signals[i], np.max(np.abs(signals[i])))
    return signals


def acquire_signals(files):
    # Signal processing parameters
    fc_low = 100
    fc_high = 10000
    ref_fc_low = 11000
    ref_fc_high = 15000
    filter_order = 5
    clip_size = 1

    # Extracts signals from wav files
    signals = [[] for _ in range(2 * len(files))]
    for i in range(len(files)):
        (fs, sig) = wavfile.read(files[i])
        signals[2 * i] = sig[:, 0]
        signals[2 * i + 1] = sig[:, 1]
    signals = np.array(signals, dtype='float')

    # Processes signals
    ref_signals = np.copy(signals)
    signals = process_signals(signals, fs, fc_low, fc_high, filter_order, clip_size)
    ref_signals = process_signals(ref_signals, fs, ref_fc_low, ref_fc_high, filter_order, clip_size)
    return signals, ref_signals, fs
