from scipy.io import wavfile
import numpy as np
from numpy import*
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter


def butter_filter(data, low, high,order, nyq): 
    low = low/nyq
    high = high/nyq
    # Get the filter coefficients 
    b, a = butter(order, high, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

def main():
    (fs, x) = wavfile.read("recording_1.wav") # Raspberry Pi one
    (fs, y) = wavfile.read("recording_2.wav")  # Raspberry Pi two
    t= np.arange(0,10,1/fs)
    T = 5.0
    high_cutoff = 6000 # cutoff frequency
    low_cutoff = 500
    nyq = 0.5*fs
    order = 1
    x= x/np.max(np.abs(x)) # normalizing the audio
    m1 = x[:,0] # microphone 1
    m2 = x[:,1] # microphone 2
    m3 = y[:,0] # microphone 3
    m4 = y[:,1] # microphone 4

    m1_filtered = butter_filter(m1, low_cutoff,high_cutoff,order, nyq) # applying low pass filter to audio signal
    m2_filtered = butter_filter(m2,low_cutoff,high_cutoff,order, nyq) # applying low pass filter to audio signal
    m3_filtered = butter_filter(m3,low_cutoff,high_cutoff,order, nyq) # applying low pass filter to audio signal
    m4_filtered = butter_filter(m4,low_cutoff,high_cutoff,order, nyq) # applying low pass filter to audio signal
    plt.subplot(4,1,1)
    plt.plot(t,m1_filtered) # plot filtered signal
    plt.subplot(4,1,2)
    plt.plot(t,m2_filtered) # plot filtered signal
    plt.subplot(4,1,3)
    plt.plot(t,m3_filtered) # plot filtered signal
    plt.subplot(4,1,4)
    plt.plot(t,m4_filtered) # plot filtered signal
    plt.show()

if __name__ == "__main__":
    main()