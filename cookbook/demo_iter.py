#!/usr/bin/env python
#!-*-coding:utf-8-*-

class Counter(object):

    def __init__(self):
        self.count = 0

    def increase(self, addend=1):
        self.count += addend


class Counter_Demo(object):
    count = 0

    def increase(self, addend=1):
        self.count += addend


    


if __name__=="__main__":
    counter = Counter()