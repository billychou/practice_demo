#!/usr/bin/env python
# -*- coding: utf-8  -*-
__version__ = "1.0"
__license__ = "Copyright (c) 2013, Shunping Jiang, All rights reserved."
__author__ = "shunping.jiang@autonavi.com"

from sensitive_words import WORDS


class SensitiveFilter(object):
    def __init__(self):
        self.d = {}

    def set(self, keywords):
        p = self.d
        q = {}
        k = ''
        for word in keywords:
            word += chr(11)
            p = self.d
            for char in word:
                char = char.lower()
                if p == '':
                    q[k] = {}
                    p = q[k]
                if not (char in p):
                    p[char] = ''
                    q = p
                    k = char
                p = p[char]

    '''
    Recommended to use cache
    '''

    def load(self):
        # _cache = Cache()
        # _data  = _cache.get("China_Censor_Words")
        # if _data:
        # self.d = _data
        # else:
        _words = [x["word"] for x in WORDS]
        self.set(_words)
        # _cache.set("China_Censor_Words", self.d, 3600*24*30)

    def replace(self, text, mask):
        p = self.d
        i = 0
        j = 0
        z = 0
        result = []
        ln = len(text)
        while i + j < ln:
            t = text[i + j].lower()
            if not (t in p):
                j = 0
                i += 1
                p = self.d
                continue
            p = p[t]
            j += 1
            if chr(11) in p:
                p = self.d
                result.append(text[z:i])
                result.append(mask)
                i = i + j
                z = i
                j = 0
        result.append(text[z:i + j])
        return "".join(result)

    def check(self, text):
        if not self.d:
            self.load()
        p = self.d
        i = 0
        j = 0
        result = []
        ln = len(text)
        while i + j < ln:
            t = text[i + j].lower()
            if not (t in p):
                j = 0
                i += 1
                p = self.d
                continue
            p = p[t]
            j += 1
            if chr(11) in p:
                p = self.d
                result.append((i, j, text[i:i + j]))
                i = i + j
                j = 0
        return result


def sample():
    filter = SensitiveFilter()
    filter.load()
    result = filter.check("SB")
    print result