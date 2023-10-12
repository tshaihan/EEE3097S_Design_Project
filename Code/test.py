import numpy as np
import signal_acquisition
import synchronisation
import time_delay_estimation
import triangulation
import matplotlib.pyplot as plt


def plot_signals(t, signals, xlabel='time (s)', ylabel='amplitude'):
    fig, ax = plt.subplots(len(signals), 1)
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)
    for i in range(len(signals)):
        ax[i].plot(t, signals[i])
    plt.show()
    return


def main():
    c = 343

    src_signals, ref_signals, fs, raw_signals, raw_fs = signal_acquisition.acquire_signals(['recording_1.wav', 'recording_2.wav'])

    t = np.linspace(0, len(src_signals[0]) / fs, len(src_signals[0]))
    plot_signals(t, src_signals)
    plot_signals(t, ref_signals)

    src_signals, delays, cross_correlations, lags = synchronisation.synchronise(src_signals, ref_signals, fs)
    plot_signals(t, src_signals)
    plot_signals(lags[0], cross_correlations, 'time delays (s)')
    print(delays)

    delays, cross_correlations, lags = time_delay_estimation.tdoa(src_signals, fs)
    plot_signals(lags[0], cross_correlations, 'time delays (s)')
    print(delays)

    d12, d13, d14 = delays * c
    position, p0 = triangulation.triangulate([0, 0], [0, 0.5], [0.8, 0.5], [0.8, 0], d12, d13, d14)
    print(position)


if __name__ == '__main__':
    main()
