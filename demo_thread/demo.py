#!/usr/bin/env python
import threading
import Queue
import time

class Blarg(threading.Thread):
    def run(self):
        print time.time()

def worker(ip):
    print "test for use",ip
    print time.time()    

for i in xrange(1,10):
    t = threading.Thread(target=worker, args=(i,))
    t.start()

