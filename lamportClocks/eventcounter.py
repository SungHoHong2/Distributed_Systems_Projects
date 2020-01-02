#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import threading

class EventCounter:
	"""
	EventCounter
	Increment the event counter if
	a) local event happens,
	b) sends message to target node
	c) receives message to target node.
	Using a lock to read/write to the value.

	"""

	def __init__(self):
		# init the lock
		self.lock = threading.Lock()
		# init the counter
		self.value = 0

	def increment(self):
		# acquire the lock
		self.lock.acquire()
		try:
			# increment the counter by one
			self.value = self.value + 1
		finally:
			# release the lock
			self.lock.release()

	def getValue(self):
		# acquire the lock
		self.lock.acquire()
		try:
			# get the value of the counter
			return self.value
		finally:
			# release the lock
			self.lock.release()

