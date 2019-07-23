#!/usr/bin/env python

L = [x*x for x in range(10)]
print(L)

g = (x*x for x in range(10))
print(g)

for i in g:
    print i


##############


