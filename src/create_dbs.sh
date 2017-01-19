#!/bin/bash
set -x
set -e
# Create pickle DBs (non-normalized)
# Assuming that this script is run from /src folder.
# This script will use every *.wav and *.mid file it can find recursively in this directory.
# This is supposed to be ran once, as non-normalized PV extraction is a standard procedure, also requires a lot of time

# Delete previous pickle files
# (Now necessary as we save in append mode)
find . -iname "*.pickle" -print0| xargs -0 rm -f

# Delete previous pitch vector files.
# Note: xargs -0 seems to be faster than find -exec since there are a lot of files.
find . \( -iname "*.pv" -o -iname "*.mpv" -o -iname "*.npv" \) -print0 | xargs -0 rm -f

# Create the '.pickle' file without normalization for *.mid files.
find . \( -iname "*.mid" -o -iname "*.midi" \) > midi-list.txt
./pitch_vectors.py midi-extract --pickle --pickle-database "./midi.pickle" midi-list.txt
rm midi-list.txt

# Create the '.pickle' file without normalization for *.wav files.
find . -iname "*.wav" > wave-list.txt
set +x  # Turn of traces because the next command is huge.
./pitch_vectors.py wav-extract --pickle --pickle-database "./wave.pickle" wave-list.txt
rm wave-list.txt
