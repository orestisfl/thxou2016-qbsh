#!/usr/bin/env python3

import sys
import numpy as np
from fastdtw import fastdtw
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

file_1 = sys.argv[1]
file_2 = sys.argv[2]
pv_1 = np.array([float(line.strip()) for line in open(file_1, 'r')])
pv_2 = np.array([float(line.strip()) for line in open(file_2, 'r')])

idx = range(min(len(pv_1), len(pv_2)))

distance, path = fastdtw(pv_1, pv_2, dist=euclidean)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(idx, pv_1[idx], label=file_1)
ax.plot(idx, pv_2[idx], label=file_2)
ax.set_ylabel('Pitch value')
ax.set_xlabel('Frame index')
ax.set_title('DTW Distance: ' + str(round(distance, 2)))
ax.legend(bbox_to_anchor=(0, 1.2, 1, 0), mode='expand',
          fontsize='small', borderaxespad=0)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height * .9])
plt.show()
