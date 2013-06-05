#coding=utf-8

import threading
import Queue
import time
import sys

Qin = Queue.Queue()   #创建队列，maxsize默认为0，表示队列长度无限
Qout = Queue.Queue()
Qerr = Queue.Queue()
Pool = []  #线程池

#出错信息保存在error里面
def report_error():
    '''报错，把出现的错误put到Qerr中'''
    Qerr.put(sys.exc_info()[:2]) 

#从队列中取出元素，

def get_all_from_queue(Q):
    """从队列中取出任务"""
    try:
        while True:
			yield Q.get_nowait()  #Equivalent to get(False)
    except Queue.Empty:
	    raise StopIteration
#从队列中执行工作


def do_work_from_queue():
	while True:
		command, item = Qin.get()
		if command == 'stop':
			break
		try:
			if command == 'process':
				result = 'new' + item
			else:
				raise Value, 'Unknown command %r' % command
		except:
			report_error()
		else:
			Qout.put(result)


#制作和开始执行线程池
def make_and_start_thread_pool(number_of_threads_in_pool=5, daemons=True):
	""" Make the thread pool """
	for i in xrange(number_of_threads_in_pool):
		new_thread = threading.Thread(target=do_work_from_queue) #这个程序执行线程
		new_thread.setDaemon(daemons)  #设置为守护进程
		Pool.append(new_thread)   #把线程放到list中
		new_thread.start()  #执行线程


def request_work(data, command='process'):
	'''把Qin中增加任务，参数data，command是默认参数process '''
	Qin.put((command, data))



def get_result():
	'''输出'''
	return Qout.get()

def show_all_results():
	for result in get_all_from_queue(Qout):
		print 'Result:', result

def show_all_errors():
	for etyp, err in get_all_from_queue(Qerr):
		print 'Error:', etyp, err

def stop_and_free_thread_pool():
	for i in range(len(Pool)):
		request_work(None, 'stop')

	for existing_thread in Pool:
		existing_thread.join()
	
	del Pool[:]


if __name__ == '__main__':
	for i in ('_ba',7,'_bo'): 
	    request_work(i)

	make_and_start_thread_pool()
	stop_and_free_thread_pool()
	show_all_results()
	show_all_errors()
