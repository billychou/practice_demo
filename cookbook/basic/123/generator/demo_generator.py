#!/usr/bin/env python

L = [x*x for x in range(10)]
g = (x*x for x in range(10))

if __name__ == "__main__":
    print L
    for n in g:
        print (n)



def fib(max):
    n, a, b = 0, 0, 1
