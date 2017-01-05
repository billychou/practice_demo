#!/usr/bin/env python

from atexit import register
from random import randrange
from threading import BoundedSemaphore, Thread, Lock
from time import sleep, ctime
import json

lock = Lock()
MAX = 5
candy_tray = BoundedSemaphore(MAX)


def refill():
    lock.acquire()
    print("Refilling candy...")
    try:
        candy_tray.release()
    except ValueError:
        print("full, skipping")
    else:
        print("ok")
    lock.release()


def buy():
    lock.acquire()
    print("Buying Candy...")
    if candy_tray.acquire(False):
        print("ok")
    else:
        print("empty, skipping")
    lock.release()


def producer(loops):
    for i in xrange(loops):
        refill()
        sleep(randrange(3))


def consumer(loops):
    for i in xrange(loops):
        buy()
        sleep(randrange(3))


def _main():
    print("Starting at:", ctime())
    nloops = randrange(2, 6)
    print("The candy machine (full with %d bards)!"%MAX)
    Thread(target=consumer, args=(randrange(nloops, nloops+2), )).start()
    Thread(target=producer, args=(nloops, )).start()

@register
def _atexit():
    print("All Done at:", ctime())



if __name__=="__main__":
    _main()



