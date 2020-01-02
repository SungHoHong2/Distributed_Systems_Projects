#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import socket
import llistener
import lclock
import eventcounter

class LNode:
	"""
	Implementation of a node or process for Lamport Clocks.

	"""

	def __init__(self, events, idnum, host, port):
		# init the message size
		self.msgsize = 1024
		# init the clock
		self.clock = lclock.LClock()
		# init the events
		self.events = events
		# init the id number
		self.idnum = idnum
		# init the host
		self.host = host
		# init the port number
		self.port = port

	# get the id of the node or process
	def getID(self):
		return self.idnum

	# get the host of the node or process
	def getHost(self):
		return self.host

	# get the port number of the node or process
	def getPort(self):
		return self.port

	def listen(self):
		# init the listener
		self.listener = llistener.LListener(self.host, self.port, self.events, self.clock)
		# return the listener
		return self.listener

	# simulate local events
	def localEvent(self):
		# increase clock by one
		self.clock.increment()
		# increase event counter by one
		self.events.increment()
		# print clock
		print("lclock",self.clock.getValue())

	# simulate sending message event
	def send(self, targetid, targethost, targetport):
		# increase clock by one
		self.clock.increment()
		# a message containing sender id and Lamport clock value.
		msg = str(self.idnum) +" "+ str(self.clock.getValue())
		# create the socket
		self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# connect to the target host
		self.sender.connect((targethost, targetport))

		try:
			#send message
			self.sender.sendall(msg)
			# print the sent message.
			print("s " + str(targetid) + " " + msg.split()[1])

		except Exception as e:
			pass
		finally: 
			# close the socket
			self.sender.close()
		#increase the event counter
		self.events.increment()

		# print Lamport clock
		print("lclock",self.clock.getValue())


