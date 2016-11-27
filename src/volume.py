#!/usr/bin/env python3

# Beat tracking example
import librosa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Audio file
filename = 'data/00013.wav'

# Volume of signal
y, sr = librosa.load(filename, sr=8000 ,offset=0.0)
signal = pd.Series(y)
signal_volume_db = []
signal_volume_abs = []

for frameCounter in xrange(0, len(y)/256):
    block = signal[256 * frameCounter : 256 * frameCounter + 256]
    block_detrend = block.subtract(block.median())
    block_volume_abs = block_detrend.abs().sum()
    block_volume_db = 10 * np.log10(block_detrend.rmul(block_detrend).sum())
    signal_volume_abs.append(block_volume_abs)
    signal_volume_db.append(block_volume_db)

signal_volume_abs = pd.Series(signal_volume_abs)
signal_volume_abs.plot(use_index = True, title = 'Volume with Absolute')
plt.show()

signal_volume_db = pd.Series(signal_volume_db)
signal_volume_db.plot(use_index = True, title = 'Volume in db')

plt.show()
