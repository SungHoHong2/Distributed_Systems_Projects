#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import threading

class EventCounter:
	""" Event counter, incremented if a) local event happens, b) message is sent or c) message is received. Has a lock, because it is shared by the node and it's listener. """

	def __init__(self):
		self.lock = threading.Lock()
		self.value = 0

	def increment(self):
		self.lock.acquire()
		try:
			self.value = self.value + 1
		finally:
			self.lock.release()

	def getValue(self):
		self.lock.acquire()
		try:
			return self.value
		finally:
			self.lock.release()

