from gcc_phat import gcc_phat


def tdoa(sig1, sig2, sig3, sig4, fs=1, max_tdoa=None):
    tdoa12 = gcc_phat(sig1, sig2, fs, max_tdoa)[0]
    tdoa13 = gcc_phat(sig1, sig3, fs, max_tdoa)[0]
    tdoa14 = gcc_phat(sig1, sig4, fs, max_tdoa)[0]
    return [tdoa12, tdoa13, tdoa14]
