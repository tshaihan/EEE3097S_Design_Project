import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from signal_acquisition import acquire_signals
from time_delay_estimation import estimate_delays
from triangulation import triangulate


def bandpower(x, fs, fmin, fmax):
    f, Pxx = sp.signal.periodogram(x, fs=fs)
    ind_min = np.argmax(f > fmin) - 1
    ind_max = np.argmax(f > fmax) - 1
    return np.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


def snr(signals, fs, f_bands):
    tot_power = 0
    sig_power = 0
    for i in range(len(signals)):
        tot_power += np.mean((signals[i]) ** 2)
        for j in range(len(f_bands)):
            sig_power += bandpower(signals[i], fs, f_bands[j][0], f_bands[j][1])
    snr = 10 * np.log10((sig_power / (tot_power - sig_power)))
    return snr


def plot_signals(t, signals, title, row_labels, xlabel='Time (s)', ylabel='Amplitude', delays=None, add_annotations=False):
    fig, ax = plt.subplots(len(signals), 1)
    fig.suptitle(title)
    fig.supxlabel(xlabel)
    fig.supylabel(ylabel)
    for i in range(len(signals)):
        ax[i].plot(t, signals[i])
        ax[i].set_ylabel(row_labels[i])
        if add_annotations:
            index = int(np.argmax(signals[i]))
            x = delays[i]
            y = signals[i][index]
            ax[i].annotate('Delay: {:.3f}ms'.format(x*1000), [x, y], fontsize=12, horizontalalignment='left', verticalalignment='top')
    plt.show()


def main():
    raw_signals, processed_signals, cal_signals, src_signals, fs = acquire_signals(
        ['Recordings/(0.4,0.4)_1.wav', 'Recordings/(0.4,0.4)_2.wav'])

    f_bands = np.asarray([[1000, 5000], [6000, 10000]])
    raw_snr = snr(raw_signals, fs, f_bands)
    print('The SNR of the raw audio signals (dB):')
    print(np.round(raw_snr, 2))
    processed_snr = snr(processed_signals, fs, f_bands)
    print('The SNR of the processed audio signals (dB):')
    print(np.round(processed_snr, 2))

    sync_delays, sync_cross_correlations, sync_lags = estimate_delays(cal_signals, cal_signals[0], fs, 10)
    print('The estimated synchronisation delays (ms):')
    t1, t2, t3, t4 = np.round(sync_delays * 1000, 3)
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}'.format(t1, t2, t3, t4))

    toa_delays, toa_cross_correlations, toa_lags = estimate_delays(src_signals, src_signals[0], fs, 10)
    print('The estimated ToA delays (ms):')
    t1, t2, t3, t4 = np.round(toa_delays * 1000, 3)
    print('{:.3f}, {:.3f}, {:.3f}, {:.3f}'.format(t1, t2, t3, t4))

    tdoa = ((toa_delays[0] - toa_delays) - (sync_delays[0] - sync_delays))[1:]
    print('The estimated TDoA values (ms):')
    t12, t13, t14 = np.round(tdoa * 1000, 3)
    print('{:.3f}, {:.3f}, {:.3f}'.format(t12, t13, t14))

    c = 343
    p1 = np.asarray([0, 0])
    p2 = np.asarray([0, 0.5])
    p3 = np.asarray([0.8, 0.5])
    p4 = np.asarray([0.8, 0])
    p, p0 = triangulate(p1, p2, p3, p4, tdoa[0], tdoa[1], tdoa[2], c)
    print('The initial source position estimate (m):')
    x0, y0 = np.round(p0, 3)
    print('{:.3f}, {:.3f}'.format(x0, y0))
    print('The estimated source position (m):')
    x, y = np.round(p, 3)
    print('{:.3f}, {:.3f}'.format(x, y))

    t = np.linspace(0, len(raw_signals[0]) / fs, len(raw_signals[0]))
    title = 'Raw Audio Signals Acquired'
    row_labels = ['Mic 1', 'Mic 2', 'Mic 3', 'Mic 4']
    plot_signals(t, raw_signals, title, row_labels)
    title = 'Processed Audio Signals Acquired'
    plot_signals(t, processed_signals, title, row_labels)

    title = 'GCC-PHAT of the Audio Signals with respect to the Calibration Signal of Mic 1'
    xlabel = 'Time Lags (s)'
    plot_signals(sync_lags[0], sync_cross_correlations, title, row_labels, xlabel, delays=sync_delays, add_annotations=True)

    title = 'GCC-PHAT of the Audio Signals with respect to the Source Signal of Mic 1'
    plot_signals(toa_lags[0], toa_cross_correlations, title, row_labels, xlabel, delays=toa_delays, add_annotations=True)


if __name__ == '__main__':
    main()
