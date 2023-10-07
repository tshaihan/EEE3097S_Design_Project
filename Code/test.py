import numpy as np
import signal_acquisition
import synchronization
import time_delay_estimation
import triangulation
import matplotlib.pyplot as plt


def plot_signals(t, signals, xlabel='time (s)', ylabel='amplitude'):
    fig, ax = plt.subplots(len(signals), 1)
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)
    for i in range(len(signals)):
        ax[i].plot(t, signals[i])
        ax[i].grid(True, 'both')
    plt.show()
    return


def main():
    c = 343

    signals, ref_signals, fs = signal_acquisition.acquire_signals(['recording_1.wav', 'recording_2.wav'])

    t = np.linspace(0, len(signals[0]) / fs, len(signals[0]))
    plot_signals(t, signals)
    plot_signals(t, ref_signals)

    signals, delays, cross_correlations, lags = synchronization.synchronize(signals, ref_signals, fs)
    plot_signals(t, signals)

    delays, cross_correlations, lags = time_delay_estimation.time_delays(signals, fs)
    plot_signals(lags[0], cross_correlations, 'time delays (s)')

    d12, d13, d14 = delays * c
    position = triangulation.triangulate([0, 0], [0, 0.5], [0.8, 0.5], [0.8, 0], d12, d13, d14)
    print(position)


if __name__ == '__main__':
    main()
