#!/usr/bin/env python

def foo(*args, **kwargs):
    print args
    print kwargs
    a = kwargs.pop('a', False)
    print a
    print args
    print kwargs
    #b = kwargs.pop('b', 'default for b')
    #print b
    assert len(kwargs) == 0, "unrecognized params in %s"% ",".join(kwargs.keys())


if __name__ == "__main__":
    print foo(3, 4, 5, a=1, b=2, c=5)
