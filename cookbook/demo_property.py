#!/usr/bin/env python
# -*-coding:utf-8 -*-

class Student(object):
    """使用propery替换setter,getter"""

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")

        if value < 0 or value > 100:
            raise ValueError("Value must between 0 ~ 100")

        self._score = value



class Person(object):
    """类方法转换成类属性"""
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)



if __name__ == "__main__":
    s = Student()
    s.score = 100
    print
    s.score = 101



