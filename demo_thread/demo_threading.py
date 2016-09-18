#!/usr/bin/env python
import threading
import Queue
import time
import random

count = 0
lock = threading.Lock()

class Blarg(threading.Thread):
    def run(self):
        print time.time()

def worker(ip):
    print "test for use",ip
    print time.time()

def toAdd():
    global count, lock
    lock.acquire()
    for i in xrange(10000):
        count = count + 1
    lock.release()

for i in range(5):
    threading.Thread(target=toAdd, args=(), name='thread'+str(i)).start()

print count
#for i in xrange(1,10):
#    t = threading.Thread(target=worker, args=(i,))
#    t.start()

