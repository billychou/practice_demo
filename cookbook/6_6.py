#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Proxy(object):
    """代理的基类"""
    def __init__(self, obj):
        super(Proxy, self).__init__(obj)
        self._obj = obj
    
    def __getattr__(self, attrib):
        return getattr(self.obj, attrib)



    def make_binder(unbound_method):
        def f(self, *a, **k):
            return unbound_method(self._obj, *a, **k)
        return f


def proxy(obj, *specials):
    obj_cls = obj.__class
    key = obj_clas, specials
    cls = known_proxy_classes.get(key)
    if cls is None:
        cls = type("%sProxy"%obj_cls.__name__, (Proxy,), { })
        for name in specials:
            name = '__%s__' % name
            unbound_method = getattr(obj_cls, name)
            setattr(cls, name, make_binder(unbound_method))
        known_proxy_classes[key] = cls
    return cls(obj)



    
