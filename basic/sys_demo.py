#!/usr/bin/env python
#!-*-coding:utf-8 -*-

import sys
import traceback


def grail(x):
    raise TypeError("Already got one")

try:
    grail("a")

except:
    exc_info = sys.exc_info()
    print(exc_info[0])
    print(exc_info[1])
    print(exc_info[2])
    traceback.print_tb(exc_info[2])
