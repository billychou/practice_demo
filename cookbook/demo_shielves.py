#!/usr/bin/env python

from initdata import db
import shelve

filename = "people-shelve"
d = shelve.open(filename)
d["a"] = "a_value"
d["b"] = "b_value"

flag = d.has_key("a")
klist = d.keys()

d.close()