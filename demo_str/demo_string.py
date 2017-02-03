#!/usr/bin/env python
# coding=utf-8

string = "I love  code."
print string

str_lst = string.split(" ")

print str_lst

words = [s.strip() for s in str_lst if s != ""]

print words


a, b = 0, 1
for i in range():
    a ,b = b, a+b

print a

new_string = " ".join(words)
print new_string
