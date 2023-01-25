#!/usr/bin/env python3

import time
import logging
import psutil

class timer:

	def __init__(self,timer_name):
		
		self._start_time = None
		self._timer_name = timer_name

	def start(self):
		"""Start a new timer"""

		if self._start_time is not None:
		    raise logging.warning("Timer is running. Use .stop() to stop it")

		self._start_time = time.perf_counter()
       
	def seek(self):
		return time.perf_counter() - self._start_time

	def stop(self):
		"""Stop the timer, and report the elapsed time"""

		if self._start_time is None:
			raise logging.warning("Timer is not running. Use .start() to start it")

		elapsed_time = time.perf_counter() - self._start_time
		self._start_time = None
		print( self._timer_name + f": {elapsed_time:0.1f} seconds")

def process_check(process):
    pid = None
    pid_info = list()
    for proc in psutil.process_iter():
        pid_info.append(proc.name())
   
    if process in pid_info:pid = True
    else:					pid = False	
	
    return pid
