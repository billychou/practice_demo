#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Base(object):
    v =  1
    def __init__(self):
        pass

class BaseSlot(object):
    """类实例只能拥有x变量,并且不生成内置__dict__属性"""
    __slots__ = "x"
    v = 1
    def __init__(self):
        pass

if __name__ == "__main__":
    base = Base()
    print dir(base)
    base.x = 2
    base.y = 3
    print base.__dict__

    baseslot = BaseSlot()
    print "Next BaseSlot"
    print dir(baseslot)
    baseslot.x = 4
    print baseslot.x
    # print baseslot.__dict__