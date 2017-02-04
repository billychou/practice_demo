#!/usr/bin/env python
# -*-coding:utf-8-*-


#
#    Author: songchuan.zhou
#    Usage:
#    1. 线程:   threading
#    2. 同步原语:
#        锁
#        信号量
#    3. 队列
#

import threading
import Queue
import time
import random
from atexit import register
from random import randrange
from threading import Thread, currentThread
from time import sleep, ctime

local_school = threading.local()

from threading import Lock
lock = Lock()

class CleanOutputSet(set):
    """
        Usage: CleanOutputSet
    """
    def __str__(self):
        return ', '.join(x for x in self)

loops = (randrange(2, 5) for x in range(randrange(3, 7)))
remaining = CleanOutputSet()


def loop(nsec):
    print("Thread {} is running...".format(threading.currentThread().name))
    myname = currentThread().name
    lock.acquire()
    remaining.add(myname)
    print("[%s] Started %s"% (ctime(), myname))
    lock.release()
    sleep(nsec)
    lock.acquire()
    remaining.remove(myname)
    print("[%s] Completed %s (%d secs)"%(ctime(), myname, nsec))
    print("(remaining: %s)"%(remaining or 'None'))
    lock.release()


class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return self.name


def process_student(name):
    std = Student()
    do_task_1(std)
    do_task_2(std)


def process_student():
    print("Hello, %s(in %s)"%(local_school.student, threading.currentThread().name))

def process_thread(name):
    local_school.student = name
    process_student()


def main():
    for pause in loops:
        Thread(target=loop, args=(pause,), name="LoopThread{}".format(pause)).start()


@register
def _atexit():
    print("all Done at:", ctime())

if __name__ == "__main__":
    main()