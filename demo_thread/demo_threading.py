#!/usr/bin/env python
import threading
import Queue
import time
import random

count = 0
lock = threading.Lock()
SHARE_Q = Queue.Queue()

def worker():
    print "test for use"
    print time.time()

for i in xrange(5):
    threading.Thread(target=worker, args=(), name='thread'+str(i)).start()
    time.sleep(1)


class Timer(threading.Thread, object):
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            print "Thread Object(%d), Timer:%s\n"%(self.thread_num, time.time())
            time.sleep(self.interval)
    def stop(self):
        self.thread_stop = True

if __name__ == "__main__":
    thread1 = Timer(1, 1)
    thread2 = Timer(2, 2)
    thread1.start()
    thread2.start()
    time.sleep(10)
    thread1.stop()
    thread2.stop()
