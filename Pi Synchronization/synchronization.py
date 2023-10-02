import random
from numpy import sqrt
from numpy import linspace
from numpy import cos
from numpy import pi
from numpy import concatenate
from numpy import zeros
from gcc_phat import gcc_phat


def synchronize(sig1, sig2, sig3, sig4, refsig, fs=1, max_tdoa=None):
    refsig_len = len(refsig)
    delay1 = gcc_phat(sig1, refsig, fs, max_tdoa)[0]
    delay2 = gcc_phat(sig2, refsig, fs, max_tdoa)[0]
    delay3 = gcc_phat(sig3, refsig, fs, max_tdoa)[0]
    delay4 = gcc_phat(sig4, refsig, fs, max_tdoa)[0]
    sync_sig1 = sig1[int(delay1 * fs) + refsig_len:]
    sync_sig2 = sig2[int(delay2 * fs) + refsig_len:]
    sync_sig3 = sig3[int(delay3 * fs) + refsig_len:]
    sync_sig4 = sig4[int(delay4 * fs) + refsig_len:]
    return [[delay1, delay2, delay3, delay4], [sync_sig1, sync_sig2, sync_sig3, sync_sig4]]


def main():
    p = [0.4445, 0]
    p1 = [0, 0]
    p2 = [0.8, 0]
    p3 = [0, 0.5]
    p4 = [0.8, 0.5]

    c = 343
    fs = 48000
    f0 = 0
    f1 = 100
    refsig_f0 = 0
    refsig_f1 = 1000
    duration = 5
    max_delay = 10
    pause = 2

    delay1 = max_delay * random.random()
    delay2 = max_delay * random.random()
    delay3 = max_delay * random.random()
    delay4 = max_delay * random.random()
    delays = [delay1 + pause, delay2 + pause, delay3 + pause, delay4 + pause]

    toa1 = sqrt((p[0] - p1[0]) ** 2 + (p[1] - p1[1]) ** 2) / c
    toa2 = sqrt((p[0] - p2[0]) ** 2 + (p[1] - p2[1]) ** 2) / c
    toa3 = sqrt((p[0] - p3[0]) ** 2 + (p[1] - p3[1]) ** 2) / c
    toa4 = sqrt((p[0] - p4[0]) ** 2 + (p[1] - p4[1]) ** 2) / c

    t = linspace(0, duration, duration * fs)
    sig = cos(2 * pi * ((f1 - f0) * t ** 2 / 2 * duration + f0 * t))
    refsig = cos(2 * pi * ((refsig_f1 - refsig_f0) * t ** 2 / 2 * duration + refsig_f0 * t))

    sig1 = concatenate((zeros(int((delay1 + duration + toa1 + 2 * pause) * fs)), sig))
    sig2 = concatenate((zeros(int((delay2 + duration + toa2 + 2 * pause) * fs)), sig))
    sig3 = concatenate((zeros(int((delay3 + duration + toa3 + 2 * pause) * fs)), sig))
    sig4 = concatenate((zeros(int((delay4 + duration + toa4 + 2 * pause) * fs)), sig))
    sig1[int((delay1 + pause) * fs):int((delay1 + pause + duration) * fs)] = refsig
    sig2[int((delay2 + pause) * fs):int((delay2 + pause + duration) * fs)] = refsig
    sig3[int((delay3 + pause) * fs):int((delay3 + pause + duration) * fs)] = refsig
    sig4[int((delay4 + pause) * fs):int((delay4 + pause + duration) * fs)] = refsig
    [est_delays, sync_sigs] = synchronize(sig1, sig2, sig3, sig4, refsig, fs)

    print("Actual delay values:")
    print(delays)
    print("Estimated delay values:")
    print(est_delays)


if __name__ == "__main__":
    main()
