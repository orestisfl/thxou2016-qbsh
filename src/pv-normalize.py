#!/usr/bin/python

import os
import sys
import numpy as np

for file in sys.argv[1:]:
    filename, fileext = os.path.splitext(file)
    if fileext == '.pv':
        pv = np.array([int(line.strip()) for line in open(file, 'r')])
        avg = np.mean(pv)
        std = np.std(pv)
        npv = (pv - avg)/std
        fd = open(filename + '.npv', 'w')
        for p in npv:
            fd.write("%s\n" % p)
        fd.close()
print()