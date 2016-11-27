#!/usr/bin/env python3

# Pitch tracking based on
# https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py

import os
import sys
from aubio import source, pitch

fs = 8000 # Default MIREX WAV sampling rate
framesize = 0.032 # In seconds

# Hopsize determines how many samples we need in order to achieve desired framesize
# Winsize is (at least for now) arbitrary, 2048 seems to give best results
winsize = 2048
hopsize = int(round(fs*framesize))
# tol = 0.1

# For pitch tracking we use the YIN fundamental frequency estimator
# Reference: http://audition.ens.fr/adc/pdf/2002_JASA_YIN.pdf
pitch_tracker = pitch('yin', winsize, hopsize, fs)
pitch_tracker.set_unit('midi')
# pitch_tracker.set_tolerance(tol)

pv = []

for file in sys.argv[1:]:
    filename, fileext = os.path.splitext(file)
    if fileext == '.wav':
        print('Processing ' + filename + '.wav', end = '\r')
        signal = source(file, fs, hopsize)
        while True:
            samples, read = signal()
            pitch = pitch_tracker(samples)[0]
            confidence = pitch_tracker.get_confidence()
            # Set bad pitch values to 0
            if confidence < 0.4 or pitch < 0: pitch = 0.
            pv += [pitch]
            if read < hopsize: break # end of file reached
        fd = open(filename + '.mpv', 'w')
        for p in pv:
            fd.write("%s\n" % p)
        fd.close()
print()