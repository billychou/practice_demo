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




class Movie(object):
    def __init__(self, title, rating, runtime, budget, gross):
        self.title = title
        self.rating = rating
        self.runtime = runtime
        self.budget = budget
        self.gross = gross

        #if budget < 0:
        #    raise ValueError("Negative value not allowed %s" % budget)
        #self.budget = budget
        #  只有在__init__方法中捕获错误的数据,但对于已经存在的类实例就无能为力了。


    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        if value < 0:
            raise ValueError("Negative value not allowed: %s" % value)
        self._budget = value

    def profit(self):
        return self.gross - self.budget


if __name__ == "__main__":
    s = Student()
    s.score = 100
    print
    s.score = 101



