from gcc_phat import gcc_phat
import matplotlib.pyplot as plt


def synchronize(sig1, sig2, sig3, sig4, refsig, duration, fs=1, max_delay=None):
    delay1 = gcc_phat(sig1, refsig, fs, max_delay)[0]
    delay2 = gcc_phat(sig2, refsig, fs, max_delay)[0]
    delay3 = gcc_phat(sig3, refsig, fs, max_delay)[0]
    delay4 = gcc_phat(sig4, refsig, fs, max_delay)[0]
    sync_sig1 = sig1[int((delay1+duration) * fs):]
    sync_sig2 = sig2[int((delay2+duration) * fs):]
    sync_sig3 = sig3[int((delay3+duration) * fs):]
    sync_sig4 = sig4[int((delay4+duration) * fs):]
    return [[delay1, delay2, delay3, delay4], [sync_sig1, sync_sig2, sync_sig3, sync_sig4]]
