#!/usr/bin/env python
from __future__ import division
import random
import itertools

#ita
def range(start, end=None, inc=1.0):
    if end is None:
        end = start + 0.0
        start = 0.0
    assert inc
    for i in itertools.count():
        next = start + i * inc
        if (inc>0.0 and next>=end) or (inc<0.0 and next<=end):
            break
        yield next

score = [random.randint(0, 100) for i in range(40)]
print score
num = len(score)
ave_num = sum(score)/len(score)
less_num = len([i for i in score if i < ave_num])
print less_num

if __name__=="__main__":
    for x in range(3, 6):
        print x
