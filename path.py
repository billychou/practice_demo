#!/usr/bin/evn python
# -*- coding:utf-8 -*-
import os 
ABS_PATH = os.path.abspath(__file__)
ROOT_PATH = os.path.dirname(ABS_PATH)
print ABS_PATH
print ROOT_PATH

RESULT = os.path.abspath(os.path.join(ROOT_PATH, "../myshell"))
print RESULT
