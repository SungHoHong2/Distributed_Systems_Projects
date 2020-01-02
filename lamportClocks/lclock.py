#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import threading
import random

class LClock:
	"""
	Lamport Clock
	Update clock if
	a) local event happens,
	b) sends message to target node
	c) receives message to target node.
	Using a lock to read/write to the value.

	"""

	def __init__(self):
		# init the lock
		self.lock = threading.Lock()
		# init clock
		self.value = 0

	def compareTimes(self, other):
		# acquire the lock
		self.lock.acquire()
		try:
			# compare local clock and received clock value, take maximum of these and add one
			self.value = max(int(self.value), int(other)) + 1
			# return the current clock value
			return self.value
		finally:
			# release the lock
			self.lock.release()

	def increment(self):
		# acquire the lock
		self.lock.acquire()
		try:
			# update date the clock
			self.value = self.value + 1
		finally:
			# release the lock
			self.lock.release()


	def getValue(self):
		# acquire the lock
		self.lock.acquire()
		try:
			# return the current clock value
			return self.value
		finally:
			# release the lock
			self.lock.release()

