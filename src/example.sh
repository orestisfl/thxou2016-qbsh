#!/bin/bash
set -x
set -e
# Example using pitch_vectors.py and search.py
# Assuming that this script is run from /src folder.
# This script will use every *.wav and *.mid file it can find recursively in this directory.

# Delete previous pitch vector files.
# Note: xargs -0 seems to be faster than find -exec since there are a lot of files.
find . \( -iname "*.pv" -o -iname "*.mpv" -o -iname "*.npv" \) -print0 | xargs -0 rm -f

# Create the '.pickle' file without normalization for *.mid files.
find . \( -iname "*.mid" -o -iname "*.midi" \) -print0 | xargs -0 ./pitch_vectors.py midi-extract --pickle --pickle-database "./midi.pickle"
# Normalize *.pv files produced by previous command.
find . -iname "*.pv" -print0 | xargs -0 ./pitch_vectors.py preprocess --pickle --pickle-database "./midi-normalized.pickle"
# Extract pitch vectors from *.wav files. This will take long (~10 minutes).
# Also pass '--preprocess' to directly preprocess pitch vectors.
find . -iname "*.wav" -print0 | xargs -0 ./pitch_vectors.py wav-extract --pickle --preprocess --pickle-database "./wav-normalized.pickle"

# Pass all 00031.npv as arguments in search. Without normalizing.
# find . -iname "00031.npv" -print0 | xargs -0 ./search.py --pitch-file --database "./midi-normalized.pickle"
# Same but with normalizing the pitch vectors first.
#find waveFile/ -iname "00031.pv" -print0 | xargs -0 ./search.py --preprocess --pitch-file --database "./midi.pickle"


# Start searching in .wav database. This will take way too long with the current implementation.
# It's the last command so you'll probably want to ctrl+c it after a while.
./search.py --pickle-whole --database "./midi-normalized.pickle" "./wave-normalized.pickle"
