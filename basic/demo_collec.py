#!/usr/bin/env python
# -*-coding:utf-8-*-
from collections import OrderedDict

d = OrderedDict([('first', 1),
                 ('second', 2),
                 ('third', 3)])

print(type(d.items))
print(d.items())


d['second'] = 4
print(d.items())

od = OrderedDict([(x,0) for x in range(20)])
print(od)


seasons = ['Spring', 'Summer', 'Fall', 'Wintter']
print(list(seasons))
print(list(enumerate(seasons)))


def demo_enumerate(sequence, start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1


x = 1
print(eval('x+1'))

#file类型的构造函数
# if isinstance("a", file):
#     result = True
# else:
#     result = False


key = lambda a: a+2
add_p = lambda a, b: a + b
print(key(2))

#language
result = True if isinstance("a", file) else False
print(result)

