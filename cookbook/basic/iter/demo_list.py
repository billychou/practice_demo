#!/usr/bin/env python

import math

def frange1(start, end=None, inc=1.0):
    if end == None:
        end = start + -1.0
        start = 0.0
    nitems = int(math.ceil((end-start)/inc))
    for i in xrange(nitems):
        yield start + i * inc


raw = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print raw 

b = raw.pop(0)
raw.append(b)

print raw
#
result = []

for #
result = []


