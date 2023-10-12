import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, firwin, minimum_phase, upfirdn


# Processes audio signals
def process_signals(signals, fs, filter_order, fc_low, fc_high, clip_size, upsample):
    signals = np.copy(signals)
    processed_signals = np.empty((len(signals), len(signals[0])*upsample))
    # Applies processing to each signal
    for i in range(len(signals)):
        # Applies Filter
        sos = butter(filter_order, [fc_low, fc_high], btype='bandpass', output='sos', fs=fs)
        signals[i] = sosfilt(sos, signals[i])
        # Removes beginning portions of signals
        signals[i][:int(clip_size * fs * upsample)] = 0
        # Normalizes signals
        signals[i] = np.divide(signals[i], np.max(np.abs(signals[i])))
        # Upsamples signals
        t1 = np.linspace(0, len(signals[i])/fs, len(signals[i]))
        t2 = np.linspace(0, len(signals[i])/fs, len(processed_signals[i]))
        processed_signals[i] = np.interp(t2, t1, signals[i])
    return processed_signals


# Extracts and processes audio signals
def acquire_signals(files):
    # Signal processing parameters
    filter_order = 1
    scr_fc_low = 100
    src_fc_high = 5000
    ref_fc_low = 10000
    ref_fc_high = 15000
    clip_size = 0.5
    upsample = 2

    # Extracts signals from wav files
    signals = [[] for _ in range(2 * len(files))]
    for i in range(len(files)):
        (fs, sig) = wavfile.read(files[i])
        signals[2 * i] = sig[:, 0]
        signals[2 * i + 1] = sig[:, 1]
    signals = np.array(signals, dtype='double')

    # Processes signals
    src_signals = process_signals(signals, fs, filter_order, scr_fc_low, src_fc_high, clip_size, upsample)
    ref_signals = process_signals(signals, fs, filter_order, ref_fc_low, ref_fc_high, clip_size, upsample)

    return src_signals, ref_signals, fs*upsample, signals, fs
