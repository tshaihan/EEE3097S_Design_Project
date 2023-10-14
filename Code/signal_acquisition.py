import numpy as np
from scipy.io import wavfile
from scipy.signal import windows, butter, sosfilt


# Processes audio signals
def process_signals(signals, filter_order, fc_low, fc_high, fs=1):
    signals = np.copy(signals)
    # Applies processing to each signal
    for i in range(len(signals)):
        # Applies Hann window
        hann = windows.hann(len(signals[i]))
        signals[i] *= hann

        # Applies Butterworth Bandpass Filter
        sos = butter(filter_order, [fc_low, fc_high], btype='bandpass', output='sos', fs=fs)
        signals[i] = sosfilt(sos, signals[i])

        # Normalises signal
        signals[i] /= np.max(signals[i])

    return signals


# Extracts and processes audio signals
def acquire_signals(files):
    # Signal processing parameters
    filter_order = 6
    fc_low1 = 1000
    fc_high1 = 5000
    fc_low2 = 6000
    fc_high2 = 10000

    # Extracts audio signals from wav files
    raw_signals = [[] for _ in range(2 * len(files))]
    for i in range(len(files)):
        (fs, sig) = wavfile.read(files[i])
        raw_signals[2 * i] = sig[:, 0]
        raw_signals[2 * i + 1] = sig[:, 1]
    raw_signals = np.asarray(raw_signals, dtype='float')

    # Processes audio signals
    mid = int((np.size(raw_signals)) / (len(raw_signals) * 2))
    cal_signals = raw_signals[:, :mid]
    src_signals = raw_signals[:, mid:]
    cal_signals = process_signals(cal_signals, filter_order, fc_low2, fc_high2, fs)
    src_signals = process_signals(src_signals, filter_order, fc_low1, fc_high1, fs)
    processed_signals = np.concatenate([cal_signals, src_signals], axis=1)

    return raw_signals, processed_signals, cal_signals, src_signals, fs
