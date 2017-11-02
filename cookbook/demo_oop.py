#!/usr/bin/env python
#-*-coding:utf-8-*-
#@Time: 17/11/2下午10:41
#@Author: songchuan.zhou@alibaba-inc.com

class Person(object):
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job


if __name__ == "__main__":
    bob = Person('Bob Smith', 17, 25000, "Software")
    sue = Person('Bob Smith 2', 27, 35000, "Hardware")

    print(bob.name.split()[-1])
    sue.pay *= 1.1
    print(sue.pay)