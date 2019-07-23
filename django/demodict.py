#!/usr/bin/env python
#! coding:utf-8


class CaseInsenstiveDict(dict):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self[key.lower()] = value

    def __contains__(self, key):
        return super(CaseInsenstiveDict, self).__contains__(key.lower())

    def __getitem__(self, key):
        return super(CaseInsenstiveDict, self).__getitem__(key.lower())

    def __setitem__(self, key, value):
        super(CaseInsenstiveDict, self).__setitem__(key.lower(), value)



if __name__ == "__main__":
    d = CaseInsenstiveDict(SpAm='eggs')
    print 'spam' in d