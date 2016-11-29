#!/usr/bin/env python3
import numpy as np


def normalize(pitch_vector):
    pitch_vector = pitch_vector[pitch_vector != 0]
    avg = np.mean(pitch_vector)
    std = np.std(pitch_vector)
    return (pitch_vector - avg) / std


def load_pitch_vector(filename):
    with open(filename) as file_object:
        return np.array([float(line.strip()) for line in file_object])


def main():
    file_list = sys.argv[1:]
    for filename in tqdm(file_list):
        base_name, fileext = os.path.splitext(filename)
        if fileext in ('.pv', '.mpv'):
            pv = normalize(load_pitch_vector(filename))

            # TODO use function from pv_extract_wave.py
            fd = open(base_name + '.npv', 'w')
            for p in pv:
                fd.write("%s\n" % p)
            fd.close()


if __name__ == '__main__':
    import os
    import sys
    from tqdm import tqdm
    sys.exit(main())
