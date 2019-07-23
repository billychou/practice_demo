#!/usr/bin/env python
#-*-coding:utf-8-*-
#@Time: 17/11/2下午10:41
#@Author: songchuan.zhou@alibaba-inc.com

class Person(object):
    """
    person
    """
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job


    def getlastName(self):
        return self.name.split(" ")[-1]

    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)

    def __str__(self):
        return ("<%s => %s: %s, %s>"%(self.__class__.__name__, self.name, self.job, self.pay))


class Manager(Person):
    def __init__(self, name, age, pay):
        Person.__init__(self, name, age, pay, 'manager')

    def giveRaise(self, percent, bounus=0.1):
        Person.giveRaise(self, percent + bounus)


if __name__ == "__main__":
    bob = Person('Bob Smith', 17, 25000, "Software")
    sue = Person('Bob Smith 2', 27, 35000, "Hardware")
    tom = Manager(name="Tom Suse", age=50, pay=500000)
    print(tom)
    print(bob.name.split()[-1])
    sue.pay *= 1.1
    print(sue.pay)