#!/usr/bin/env python
# -*-coding: utf-8 -*-

from weakref import WeakKeyDictionary

class NonNegative(object):
    """非负数描述符"""
    #
    #
    #
    def __init__(self, default):
        self.default = default
        self.data = WeakKeyDictionary()
        #weakref 弱引用,WeakKeyDictionary创建一个key为弱引用对象的词典


    def __get__(self, instance, owner):
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Negative value not allowed: %s" % value)
        self.data[instance] = value


class Descriptor(object):
    """
        限定name属性必须以b开头的描述符
    """
    def __init__(self):
        self._name = ''

    def __get__(self, instance, owner):
        print "Getting: %s" % self._name
        return self._name

    def __set__(self, instance, name):
        """
            :param instance:
            :param name:
            :return:
             title首字母大写
        """
        if not name.startswith("b"):
            print "exception"
            raise ValueError("the name is not started with b")
        else:
            print "非异常"
            self._name = name.title()

    def __delete__(self, instance):
        print "Deleting: %s" % self._name
        del self._name


class Movie(object):
    name = Descriptor()


if __name__ == "__main__":
    pass