#!/usr/bin/env python3

import os
import sys
import numpy as np

for file in sys.argv[1:]:
    filename, fileext = os.path.splitext(file)
    if fileext == '.pv':
        print('Processing ' + filename + '.pv', end='\r')
        pv = np.array([float(line.strip()) for line in open(file, 'r')])
        # pv = np.trim_zeros(pv)
        pv = pv[pv != 0]
        avg = np.mean(pv)
        std = np.std(pv)
        npv = (pv - avg) / std
        fd = open(filename + '.npv', 'w')
        for p in npv:
            fd.write("%s\n" % p)
        fd.close()
print()
