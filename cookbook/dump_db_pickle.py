#!/usr/bin/env python
#-*-coding:utf-8-*-
#@Time: 17/10/31下午11:45
#@Author: songchuan.zhou@alibaba-inc.

import pickle
dbfile = open("people-pickle", 'rb')  #使用python3

db = pickle.load(dbfile)
for key in db:
    print(key, "=> \n", db[key])
print(db["sue"]["name"])
