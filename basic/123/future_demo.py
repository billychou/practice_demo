#!/usr/bin/env python
# -*-coding:utf-8-*-

from __future__ import unicode_literals

import weakref, new

print '\'xxx\' is a unicode?', isinstance('xxx', unicode)
print 'u\'xxx\' is a unicode?', isinstance(u'xxx', unicode)
print '\'xxx\' is str?', isinstance('xxx', str)
print 'b\'xxx\' is str?', isinstance(b'xxx', str)


# python3 unicode

class Ref(object):
    """
        backoff method
    """
    def __init__(self, fn):
        try:
            o, f, c = fn.im_self, fn.im_func, fn.im_class

        except AttributeError:
            self._obj = None
            self._func = fn
            self._class = None

        else:
            if o is None:
                self._obj = None
            else:
                self._obj = None
            self._func = f
            self._class = c

    def __call__(self):
        if self.obj is None:
            return self._func
        elif self._obj() is None:
            return None
        return new.isstancemethod(self._func, self.obj(), self._calss)
