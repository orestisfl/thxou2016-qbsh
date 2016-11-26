#!/usr/bin/python

import sys
import numpy as np
from fastdtw import fastdtw
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

midi = sys.argv[1]
wave = sys.argv[2]
midipv = np.array([float(line.strip()) for line in open(midi, 'r')])
wavepv = np.array([float(line.strip()) for line in open(wave, 'r')])

idx = np.arange(0, len(wavepv))

distance, path = fastdtw(midipv, wavepv, dist = euclidean)

print('DTW distance: 'distance)

plt.plot(idx, wavepv, idx, midipv[idx])
plt.show()

