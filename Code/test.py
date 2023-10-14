import numpy as np
import matplotlib.pyplot as plt
from signal_acquisition import acquire_signals
from time_delay_estimation import estimate_delays
from triangulation import triangulate


def plot_signals(t, signals, xlabel='time (s)', ylabel='amplitude'):
    fig, ax = plt.subplots(len(signals), 1)
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)
    for i in range(len(signals)):
        ax[i].plot(t, signals[i])
    plt.show()
    return


def main():
    raw_signals, processed_signals, cal_signals, src_signals, fs = acquire_signals(['(0.4,0.25)_1.wav', '(0.4,0.25)_2.wav'])

    # t = np.linspace(0, len(src_signals[0]) / fs, len(src_signals[0]))
    # plot_signals(t, src_signals)
    # plot_signals(t, cal_signals)

    sync_delays, sync_cross_correlations, sync_lags = estimate_delays(cal_signals, cal_signals[0], fs, 10)
    # plot_signals(sync_lags[0], sync_cross_correlations, 'time delays (s)')
    print(sync_delays)

    toa_delays, toa_cross_correlations, toa_lags = estimate_delays(src_signals, src_signals[0], fs, 10)
    # plot_signals(tdoa_lags[0], tdoa_cross_correlations, 'time delays (s)')
    print(toa_delays)

    tdoa = ((toa_delays[0] - toa_delays) - (sync_delays[0] - sync_delays))[1:]
    print(tdoa)

    c = 343
    p1 = np.asarray([0, 0])
    p2 = np.asarray([0, 0.5])
    p3 = np.asarray([0.8, 0.5])
    p4 = np.asarray([0.8, 0])

    position, p0 = triangulate(p1, p2, p3, p4, tdoa[0], tdoa[1], tdoa[2], c)
    print(p0)
    print(position)


if __name__ == '__main__':
    main()
