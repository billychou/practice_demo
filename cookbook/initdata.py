#!/usr/bin/env python
#-*-coding:utf-8-*-
#@Time: 17/10/29下午5:11
#@Author: songchuan.zhou@alibaba-inc.com


bob = {'job': 'dev', 'pay': 30000, 'age': 42, 'name': 'Bob Smith'}
sue = {'job': 'hdw', 'pay': 40000, 'age': 45, 'name': 'Sue Jones'}
tom = {'job': None, 'pay': 0, 'age': 50, 'name': 'Tom'}

db = {}
db['bob'] = bob
db['sue'] = sue
db['tom'] =tom

if __name__ == "__main__":
    for key in db:
        print(key, '=>\n', db[key])