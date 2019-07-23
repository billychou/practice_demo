#!/usr/bin/env python
#-*-coding:utf-8-*-
#@Time: 17/11/9下午8:48
#@Author: songchuan.zhou@alibaba-inc.com

from functools import wraps

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print("called decorated function")
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    print("Called example function")

example()