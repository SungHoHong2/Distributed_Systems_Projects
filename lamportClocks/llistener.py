#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import socket
import threading
import eventcounter
import traceback

class LListener():
	""" Listener for a Lamport Clocks node, so that listening can happen in its own thread. The clock is shared by listener and node instances, so the listener can increment clock, when it gets a message. Uses classes LClock and EventCounter."""

	def __init__(self, host, port, events, clock):

		# threading.Thread.__init__(self)
		self.clock = clock
		self.events = events
		self.host = host
		self.port = port
		self.msgsize = 1024

		self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# self.listener.settimeout(10)
		self.listener.bind((self.host, self.port))
		self.listener.listen(10)

	def recieveMsg(self):

		try:
			# print("recieveMsg step 0")
			clientsocket, address = self.listener.accept()

			# print("recieveMsg step 1")

			msg = clientsocket.recv(self.msgsize)
			clientsocket.close()

			# print("recieveMsg step 2")

			# Received timestamp from the server
			self.clock.increment()
			n = self.clock.compareTimes(msg.split()[1])
			self.events.increment()

			# Printing for receiving the message.
			print("r " + msg + " " + str(n))
			print("lclock", self.clock.getValue())

		except socket.error as e:
			running = 0

		return


	# def run(self):
	# 	running = 1
	# 	while running:
	# 		try:
	# 			clientsocket, address = self.listener.accept()
	# 			msg = clientsocket.recv(self.msgsize)
	# 			clientsocket.close()
	#
	# 			# Received timestamp from the server
	# 			self.clock.increment()
	# 			n = self.clock.compareTimes(msg.split()[1])
	# 			self.events.increment()
	#
	# 			# Printing for receiving the message.
	# 			print("r " + msg + " " + str(n))
	#
	# 		except socket.error as e:
	# 			running = 0
	# 	return
