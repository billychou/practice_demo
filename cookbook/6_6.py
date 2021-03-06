#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Student(object):
    def __init__(self, name, sex, score):
        self.name = name
        self.sex = sex
        self.score = score
    
    def get_score(self):
        pass
    
    def __getattr__(self, key):
        pass

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


known_proxy_classes = {}
def proxy(obj, *specials):
    obj_cls = obj.__class__
    key = obj_cls, specials
    cls = known_proxy_classes.get(key)
    if cls is None:
        cls = type("%sProxy" % obj_cls.__name__, (Proxy,), { })
        for name in specials:
            name = '__%s__' % name
            unbound_method = getattr(obj_cls, name)
            setattr(cls, name, make_binder(unbound_method))
        known_proxy_classes[key] = cls
    return cls(obj)

if __name__ == "__main__":
    print dir(Proxy)
    print dir(Student)



    
