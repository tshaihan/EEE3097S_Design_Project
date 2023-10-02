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
