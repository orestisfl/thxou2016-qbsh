#!/usr/bin/python

import music21
import math
import os

path = 'MIR-QBSH-corpus/midiFile/'

framesize = 0.01

for file in os.listdir(path):
    filename, fileext = os.path.splitext(file)
    if fileext == '.mid':
        print('Processing ' + filename + '.mid', end = '\r')
        md = music21.converter.parse(path + filename + '.mid').flat

        p = [note.pitch.midi for note in md.notes]
        reps = [math.floor(note['durationSeconds']/framesize) for note in md.notes.secondsMap]

        # Make pv and flatten it
        pv = [item for sublist in [[e] * r for e,r in zip(p, reps)] for item in sublist]

        f = open(path + filename + '.pv', 'w')
        for p in pv:
            f.write("%s\n" % p)
        f.close()
print()