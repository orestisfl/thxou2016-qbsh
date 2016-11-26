# Beat tracking example
import librosa
import numpy as np

# Audio file
# Kai mp3 pairnei kai wav
filename = 'data/00013.wav'

# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
# offset (float32), se seconds arxizei meta apo tosa seconds
# sr (int), target sampling rate default=22050, if set to 'None' uses native sr
y, sr = librosa.load(filename, sr=None ,offset=0.0)

# Create destination file
f = open('data/zeropv.pv', 'w')


# Using zero crossing rate, frame size 256
for counter in range(0, len(y)/256):
  z = librosa.zero_crossings(y[256*counter:counter*256+256])
  #print(z)
  z1 = np.vstack([y[256*counter:counter*256+256], z]).T
  z2 = np.nonzero(z)
  f.write(str(len(z2[0])) + '\n')

f.close()
