#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708


import socket
import threading
import traceback

class LListener():
	"""
	Listener for a Lamport Clocks node

	"""

	def __init__(self, host, port,  clock):
		# init the clock
		self.clock = clock
		# init the host
		self.host = host
		# init the port
		self.port = port
		# init the messge size
		self.msgsize = 1024

		# create the socket
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# set a socket option.
		self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		# bind the host and port
		self.listener.bind((self.host, self.port))
		# enable a server to accept connections.
		self.listener.listen(10)

	# receive message
	def recieveMsg(self):

		try:
			# waiting for the message
			clientsocket, address = self.listener.accept()
			# receive the message
			msg = clientsocket.recv(self.msgsize)
			# close socket
			clientsocket.close()

			# synchronize Lamport clock with other nodes
			self.clock.increment()
			n = self.clock.compareTimes(msg.split()[1])

			# Printing for receiving the message.
			print("r " + msg + " " + str(n))
			print("lclock", self.clock.getValue())

		except socket.error as e:
			pass

		return

