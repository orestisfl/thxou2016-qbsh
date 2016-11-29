#!/usr/bin/env python3

# Pitch tracking based on
# https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py

import os
import numpy as np
from aubio import source, pitch

fs = 8000  # Default MIREX WAV sampling rate
framesize = 0.032  # In seconds

# Hopsize determines how many samples we need in order to achieve desired framesize
# Winsize is (at least for now) arbitrary, 2048 seems to give best results
winsize = 2048
hopsize = int(round(fs * framesize))
# tol = 0.1

# For pitch tracking we use the YIN fundamental frequency estimator
# Reference: http://audition.ens.fr/adc/pdf/2002_JASA_YIN.pdf
pitch_tracker = pitch('yin', winsize, hopsize, fs)
pitch_tracker.set_unit('midi')
# pitch_tracker.set_tolerance(tol)


def pitch_vector_from_wav(filename):
    pv = []
    signal = source(filename, fs, hopsize)
    while True:
        samples, read = signal()
        pitch = pitch_tracker(samples)[0]
        confidence = pitch_tracker.get_confidence()
        # Set bad pitch values to 0
        if confidence < 0.4 or pitch < 0:
            pitch = 0.
        pv.append(pitch)
        if read < hopsize:
            return np.array(pv)


def save_pitch_vector(pitch_vector, filename):
    with open(filename, 'w') as file_object:
        print('\n'.join(str(p) for p in pitch_vector), file=file_object)


def main():
    # TODO: proper argparse
    file_list = sys.argv[1:]
    for filename in tqdm(file_list):
        base_name, extension = os.path.splitext(filename)
        if extension.lower() == '.wav':
            pitch_vector = pitch_vector_from_wav(filename)
            save_pitch_vector(pitch_vector, base_name + '.mpv')
        else:
            print("{} supports only files ending with '.wav'".format(sys.argv[0]), file=sys.stderr)
    return 0

if __name__ == '__main__':
    import sys
    import pickle
    from tqdm import tqdm
    sys.exit(main())
