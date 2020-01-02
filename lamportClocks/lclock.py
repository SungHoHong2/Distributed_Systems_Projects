#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import threading
import random

class LClock:
	""" Lamport Clock with lock, because it is shared between node and node's listener for incoming messages."""

	def __init__(self):
		self.lock = threading.Lock()
		self.value = 0

	def compareTimes(self, other):
		self.lock.acquire()
		try:
			self.value = max(int(self.value), int(other)) + 1
			return self.value
		finally:
			self.lock.release()

	def increment(self):
		self.lock.acquire()
		try:
			self.value = self.value + 1
		finally:
			self.lock.release()

	def incrementRandom(self):
		# r = random.randint(1,5)
		r = 1
		self.lock.acquire()
		try:
			self.value = self.value + r
			# Printing for local event.
			print("l " + str(r))
		finally:
			self.lock.release()

	def getValue(self):
		self.lock.acquire()
		try:
			return self.value
		finally:
			self.lock.release()

