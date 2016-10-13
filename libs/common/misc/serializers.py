#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import cPickle as pickle
except ImportError:
    import pickle
import json


class PickleSerializer(object):
    """ pickle serializer except int """
    def dumps(self, obj):
        if not isinstance(obj, int) or isinstance(obj, bool):
            return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
        else:
            return obj

    def loads(self, obj):
        try:
            value = int(obj)
        except (ValueError, TypeError):
            value = pickle.loads(obj)
        return value


class JsonSerializer(object):
    """ json serializer except int """
    def dumps(self, obj):
        return json.dumps(obj, separators=(',', ':')).encode('latin-1')

    def loads(self, data):
        return json.loads(data.decode('latin-1'))


class DummySerializer(object):
    """ dummy serializer do nothing """
    def dumps(self, obj):
        return obj

    def loads(self, obj):
        return obj
