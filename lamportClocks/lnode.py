#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import socket
import llistener
import lclock
import eventcounter

class LNode:
	""" Implementation of a node or process for Lamport Clocks. Uses classes LListener, LClock and EventCounter. """

	def __init__(self, events, idnum, host, port):

		self.msgsize = 1024

		self.clock = lclock.LClock()
		self.events = events
		self.idnum = idnum
		self.host = host
		self.port = port

	def getID(self):
		return self.idnum

	def getHost(self):
		return self.host

	def getPort(self):
		return self.port

	def listen(self):
		self.listener = llistener.LListener(self.host, self.port, self.events, self.clock)
		# self.listener.start()
		return self.listener

	def localEvent(self):
		""" Have a simulated local event, increase Lamport clock by a random amount (1-5). """
		self.clock.increment()
		self.events.increment()

		print("lclock",self.clock.getValue())


	def send(self, targetid, targethost, targetport):
		""" Send a message containing sender id and Lamport clock value. """
		self.clock.increment()

		msg = str(self.idnum) +" "+ str(self.clock.getValue())

		self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sender.connect((targethost, targetport))

		try:
			self.sender.sendall(msg)
			# Printing for sent message.
			print("s " + str(targetid) + " " + msg.split()[1])

		except Exception as e:
			pass
		finally: 
			self.sender.close()

		self.events.increment()


		print("lclock",self.clock.getValue())


