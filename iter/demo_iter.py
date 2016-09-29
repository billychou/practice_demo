#!/usr/bin/env python
import itertools

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


if __name__=="__main__":
    for x in range(3, 6):
        print x
