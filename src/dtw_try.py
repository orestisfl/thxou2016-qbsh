#!/usr/bin/env python3

import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw

pitch_vector_1 = []
pitch_vector_2 = []

f1 = open("data/00013.pv", "r")
for line in f1:
  pitch_vector_1.append(float(line.rstrip()))

f2 = open("data/zeropv.pv", "r")
for line in f2:
  pitch_vector_2.append(float(line.rstrip()))

#print pitch vectors
print "Pitch Vector 1"
print pitch_vector_1

print "Pitch Vector 2"
print pitch_vector_2

distance, path = fastdtw(pitch_vector_1, pitch_vector_2, dist=euclidean)
print "Distance is : " + str(distance)

f1.close()
f2.close()