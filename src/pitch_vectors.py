#!/usr/bin/env python3
import math
from collections import namedtuple
import numpy as np
from aubio import source, pitch
import music21

fs = 8000  # Default MIREX WAV sampling rate
framesize = 0.032  # In seconds

# Pitch tracking based on
# https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py

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


def main():
    options = parse_args(sys.argv[1:])
    if options is None:
        return 1
    else:
        action, options = options

    if options.pickle:
        import pickle
        pickle_pvs = {}
    target_extension = action.target_extension
    if options.normalize:
        target_extension = '.npv'
    for filename in tqdm(options.files):
        base_name, fileext = os.path.splitext(filename)
        if action.extension_check(fileext):
            pv = action.get_pv(filename)
            if options.normalize:
                pv = preprocess(pv)
            save_pitch_vector(pv, base_name + target_extension)
            if options.pickle:
                pickle_pvs[filename] = pv
        else:
            print("{} {} doesn't support extension '{}'.".format(sys.argv[0], action.name, fileext), file=sys.stderr)
    if options.pickle:
        with open(options.pickle_database, 'wb') as file_object:
            pickle.dump(pickle_pvs, file_object)
    return 0


def parse_args(args):
    action = args.pop(0) if args else ''
    try:
        action = ACTION_NAMES.index(action)
        action = ACTIONS[action]
    except ValueError:
        print("Action {} not found. Valid options: {}".format(action, ', '.join(ACTION_NAMES)), file=sys.stderr)
        return None

    import argparse
    parser = argparse.ArgumentParser(prog=sys.argv[0] + ' ' + action.name)
    is_normalize = (action.name == 'preprocess')
    parser.add_argument('files', type=str, nargs='+', help="List of files to be processed.")
    parser.add_argument(
        '--preprocess', '-n',
        default=is_normalize,
        action='store_true',
        help='Normalize extracted pitch vectors.')
    parser.add_argument(
        '--recursive', '-r',
        default=False,
        action='store_true',
        help='Recursively visit files in directories.#TODO'
    )
    parser.add_argument(
        '--pickle', '-p',
        default=False,
        action='store_true',
        help='Save result as pickle file.'
    )
    parser.add_argument(
        "--pickle-database", "-d",
        metavar="PICKLE FILE",
        type=str,
        default=None,
        help="Pickle where results should be stored. Requires '--pickle'."
    )

    # Validate
    options = parser.parse_args(args)
    if options.recursive:
        raise NotImplementedError("--recursive")
    if options.pickle and not options.pickle_database:
        options.pickle_database = 'database-{}.pickle'.format(action.name)
    elif options.pickle_database and not options.pickle:
        parser.error("'--pickle-database' requires '--pickle'.")

    return action, options


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


def pitch_vector_from_midi(filename):
    md = music21.converter.parse(filename).flat
    p = [note.pitch.midi for note in md.notes]
    reps = [math.floor(note['durationSeconds'] / framesize) for note in md.notes.secondsMap]
    # Make pv and flatten it
    pv = [item for sublist in [[e] * r for e, r in zip(p, reps)] for item in sublist]
    return np.array(pv)


def save_pitch_vector(pitch_vector, filename):
    with open(filename, 'w') as file_object:
        print('\n'.join(str(p) for p in pitch_vector), file=file_object)


def preprocess(pitch_vector):
    # Remove leading and trailing zeros
    pitch_vector = np.trim_zeros(pitch_vector)

    # Mark everything outside +/- T1 semitones from the mean as unvoiced (0), here T1 = 20
    T1 = 20
    mean = np.mean(pitch_vector)
    pitch_vector[pitch_vector >= mean + T1] = 0
    pitch_vector[pitch_vector <= mean - T1] = 0

    # The jumps between 2 consecutive frames cannot be more than +/- T2 semitones, here T2 = 15
    T2 = 15
    for i, pitch in enumerate(pitch_vector[:-2]):
        diff = pitch_vector[i + 1] - pitch
        if diff > T2:
            pitch_vector[i + 1] = pitch + np.sign(diff) * T2

    # Every unvoiced frame is set to the pitch of the previous voiced frame
    last_voiced = mean  # In case we start with an unvoiced frame (should be rare as we trimmed)
    for i, pitch in enumerate(pitch_vector):
        if pitch == 0:
            pitch_vector[i] = last_voiced
        else:
            last_voiced = pitch

    # Moving Average smoothing of order MA, here MA = 9
    MA = 9
    pitch_vector = np.convolve(pitch_vector, np.ones((MA,)) / MA, mode='valid')

    # Remove mean
    # pitch_vector = pitch_vector - mean
    return pitch_vector


def load_pitch_vector(filename):
    with open(filename) as file_object:
        return np.array([float(line.strip()) for line in file_object])


if __name__ == '__main__':
    import os
    import sys
    from tqdm import tqdm
    # Available actions for this script
    Action = namedtuple('Action', ['name', 'extension_check', 'get_pv', 'target_extension'])
    # TODO: action: create pickle from .pv files.
    ACTIONS = [
        Action('preprocess', (lambda ext: 'pv' in ext.lower()), load_pitch_vector, '.npv'),
        Action('wav-extract', (lambda ext: ext.lower() == '.wav'), pitch_vector_from_wav, '.pv'),
        Action('midi-extract', (lambda ext: ext.lower() in ['.midi', '.mid']), pitch_vector_from_midi, '.pv')
    ]
    ACTION_NAMES = [x.name for x in ACTIONS]
    sys.exit(main())
