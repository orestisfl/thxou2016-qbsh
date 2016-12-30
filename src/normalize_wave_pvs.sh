#!/bin/bash
set -x
set -e
# Normalize pickle DBs
# Assuming that this script is run from /src folder.

# Create normalized PVs pickle db from midi files
# find datasets/MIR-QBSH-corpus/midiFile -iname "*.pv" -print0 | xargs -0 ./pitch_vectors.py normalize --pickle --pickle-database "./midi-normalized.pickle"

# Create normalized PVs pickle db from wave files
find datasets/MIR-QBSH-corpus/waveFile -iname "*.pv" -print0 | xargs -0 ./pitch_vectors.py normalize --pickle --pickle-database "./wave-normalized.pickle"
