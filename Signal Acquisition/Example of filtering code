import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile # For reading/writing wav files
import sounddevice as sd # For playing/recording audio
from IPython import embed # For debugging

# Read the input wav file
[samplerate, audio] = scipy.io.wavfile.read('nuisance.wav')

# Get a few seconds of this audio
offset = samplerate * np.random.randint(100)
print offset
n = 32768*6
x = audio[offset:(offset+n), 0] # audio is stereo; just grab one channel

# Compute the FFT to get the frequency-domain representation
y = np.fft.fft(x)

# Experiment with various filters:

# 1) Throw away all the high frequencies
#Note that the FFT is symmetrical, and the highest frequency is halfway
# keepFraction = 20
# yMod = np.array(y)
# yMod[(n/keepFraction):-(n/keepFraction)] = 0

# 2) Throw away all the low frequencies
# keepFraction = 20
# yMod = np.array(y)
# yMod[0:(n/keepFraction)] = 0
# yMod[-(n/keepFraction):-1] = 0

# 3) Shift the frequencies (really nasty auto-tuner)
yMod = np.zeros(n, dtype=np.complex128)

for f in range(n / 2):
  oldfreq = 0.95 * f
  yMod[f] = y[np.floor(oldfreq)]
  yMod[-f] = y[-np.floor(oldfreq)]
  # yMod[f] = y[min(f + 1000, n/2)]
  # yMod[-f] = y[-min(f + 1000, n/2)]


# Plot the results, if they're small enough
if n < 10000:
  plt.plot(np.real(y))
  plt.plot(np.real(yMod))
  plt.show()

# Play the input and result for comparison
sd.play(x, samplerate)
sd.wait()

# Take the inverse FFT to get the audio back, and play it
xMod = np.real(np.fft.ifft(yMod)).astype(np.int16)
sd.play(xMod, samplerate)
sd.wait()

