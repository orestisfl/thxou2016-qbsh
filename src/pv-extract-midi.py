#!/usr/bin/python

import os
import sys
import math
import music21

framesize = 0.032

for file in sys.argv[1:]:
    filename, fileext = os.path.splitext(file)
    if fileext == '.mid':
        print('Processing ' + filename + '.mid', end = '\r')
        md = music21.converter.parse(filename + '.mid').flat

        p = [note.pitch.midi for note in md.notes]
        reps = [math.floor(note['durationSeconds']/framesize) for note in md.notes.secondsMap]

        # Make pv and flatten it
        pv = [item for sublist in [[e] * r for e,r in zip(p, reps)] for item in sublist]

        f = open(filename + '.pv', 'w')
        for p in pv:
            f.write("%s\n" % p)
        f.close()
print()