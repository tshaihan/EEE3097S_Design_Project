from numpy import sqrt
from numpy import linspace
from numpy import cos
from numpy import pi
from numpy import concatenate
from numpy import zeros
from gcc_phat import gcc_phat


def tdoa(sig1, sig2, sig3, sig4, fs=1, max_tdoa=None):
    tdoa12 = gcc_phat(sig1, sig2, fs, max_tdoa)[0]
    tdoa13 = gcc_phat(sig1, sig3, fs, max_tdoa)[0]
    tdoa14 = gcc_phat(sig1, sig4, fs, max_tdoa)[0]
    return [tdoa12, tdoa13, tdoa14]


def main():
    p = [0.4445, 0]
    p1 = [0, 0]
    p2 = [0.8, 0]
    p3 = [0, 0.5]
    p4 = [0.8, 0.5]

    c = 343
    max_tdoa = 0.003
    fs = 48000
    f0 = 0
    f1 = 100
    duration = 5

    t = linspace(0, duration, duration * fs)
    sig = cos(2 * pi * ((f1 - f0) * t ** 2 / 2 * duration + f0 * t))

    toa1 = sqrt((p[0] - p1[0]) ** 2 + (p[1] - p1[1]) ** 2) / c
    toa2 = sqrt((p[0] - p2[0]) ** 2 + (p[1] - p2[1]) ** 2) / c
    toa3 = sqrt((p[0] - p3[0]) ** 2 + (p[1] - p3[1]) ** 2) / c
    toa4 = sqrt((p[0] - p4[0]) ** 2 + (p[1] - p4[1]) ** 2) / c
    tdoa_values = [toa1 - toa2, toa1 - toa3, toa1 - toa4]

    sig1 = concatenate((zeros(int(toa1 * fs)), sig))
    sig2 = concatenate((zeros(int(toa2 * fs)), sig))
    sig3 = concatenate((zeros(int(toa3 * fs)), sig))
    sig4 = concatenate((zeros(int(toa4 * fs)), sig))
    est_tdoa_values = tdoa(sig1, sig2, sig3, sig4, fs, max_tdoa)

    print("Actual TDoA values:")
    print(tdoa_values)
    print("Estimated TDoA values:")
    print(est_tdoa_values)


if __name__ == "__main__":
    main()
