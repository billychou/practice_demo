#!/usr/bin/env python
#-*-coding:utf-8-*-
#@Time: 17/10/31下午11:38
#@Author: songchuan.zhou@alibaba-inc.com

from initdata import db
import pickle

dbfile = open('people-pickle', 'wb')
pickle.dump(db, dbfile)
dbfile.close()