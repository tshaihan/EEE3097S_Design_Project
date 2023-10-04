import matplotlib.pyplot as plt
from numpy import sqrt, multiply, linspace
from scipy.io import wavfile
from scipy.signal import butter, lfilter, windows


def butter_filter(sig, low, high, order=1, fs=1):
    # Get the filter coefficients
    b, a = butter(order, [low, high], btype='bandpass', analog=False, fs=fs)
    filtered_sig = lfilter(b, a, sig)
    return filtered_sig


def clip(sig, size, fs=1):
    sig = sig[int(size * fs):]
    return sig


def normalize(sig):
    sig = sig / sqrt(sum(abs(sig ** 2)) / len(sig))
    return sig


def mask(sig, threshold):
    for i in range(0, len(sig)):
        sig[i] = sig[i] if abs(sig[i]) > threshold else 0
    return sig


def window(sig):
    hanning = windows.hann(len(sig))
    sig = multiply(sig, hanning)
    return sig


def process_signals(signals, fs, fc_low, fc_high, order, clip_size, threshold):
    for i in range(len(signals)):
        signals[i] = butter_filter(signals[i], fc_low, fc_high, order, fs)
        signals[i] = clip(signals[i], clip_size, fs)
        signals[i] = normalize(signals[i])
        signals[i] = mask(signals[i], threshold)
        signals[i] = window(signals[i])
    return signals


def acquire_signals(files):
    signals = [[] for _ in range(2 * len(files))]
    for i in range(len(files)):
        (fs, sig) = wavfile.read(files[i])
        signals[2 * i] = sig[:, 0]
        signals[2 * i + 1] = sig[:, 1]

    fc_low = 200
    fc_high = 20000
    order = 2
    clip_size = 1
    threshold = 0.1

    signals = process_signals(signals, fs, fc_low, fc_high, order, clip_size, threshold)

    return signals, fs


def main():
    signals, fs = acquire_signals(["recording_1.wav", "recording_2.wav"])
    sig1, sig2, sig3, sig4 = signals

    t = linspace(0, len(sig1) / fs, len(sig1))

    plt.subplot(8, 1, 1)
    plt.plot(t, sig1)  # plot filtered signal
    plt.title("Pi 1, channel 1")
    plt.subplot(8, 1, 3)
    plt.plot(t, sig2)  # plot filtered signal
    plt.title("Pi 1, channel 2")
    plt.subplot(8, 1, 5)
    plt.plot(t, sig3)  # plot filtered signal
    plt.title("Pi 2, channel 1")
    plt.subplot(8, 1, 7)
    plt.plot(t, sig4)  # plot filtered signal
    plt.title("Pi 2, channel 2")
    plt.show()


if __name__ == "__main__":
    main()
