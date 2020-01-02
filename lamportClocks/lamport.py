import lnode
import random
import socket
import sys
import time
import eventcounter

""" Program to simulate, how Lamport Clocks work. This file contains the main and uses classes EventCounter and LNode."""

if len(sys.argv) < 2:
	print("Usage: program congfiguration_file line")
	sys.exit()

conf_file = sys.argv[1]

hosts = open(conf_file)
nodes = {}

events = eventcounter.EventCounter()

curr_host = int(sys.argv[2])


for idx, line in enumerate(hosts):
	l = line.split()
	if not l:
		continue

	# Take correct row for this node from the conf file.
	if idx == int(sys.argv[2]):
		thisnode = lnode.LNode(events, int(l[0]), l[1], int(l[2]))
		continue

	nodes[int(l[0])] = lnode.LNode(events, int(l[0]), l[1], int(l[2]))

# Time to start all the nodes needed, hopefully.
time.sleep(5)
thisListener = thisnode.listen()

# Connecting Nodes
# nodes[1] == 0
# nodes[2] == 1
# nodes[3] == 2

# p0 : a s1 r3 b
# p1 : c r2 s3
# p2 : r1 d s2 e

# p0 : a s1 r3 b
if curr_host == 0:
	print("FRISK:",curr_host, nodes)

	# a
	thisnode.localEvent()
	# time.sleep(1)

	# s1 (p0) -> r1 (p2)
	target = nodes[2+1]
	try:
		thisnode.send(target.getID(), target.getHost(), target.getPort())
	except socket.error as e:
		pass

	# time.sleep(1)

	# r3
	thisListener.recieveMsg()
	# time.sleep(1)

	# b
	thisnode.localEvent()
	# time.sleep(1)


# p1 : c r2 s3
elif curr_host == 1:
	print("CHARA:",nodes)

	# c
	thisnode.localEvent()
	# time.sleep(1)

	# r2
	thisListener.recieveMsg()
	# time.sleep(1)

	# s3 (p1) -> r3 (p0)
	target = nodes[0+1]
	try:
		thisnode.send(target.getID(), target.getHost(), target.getPort())
	except socket.error as e:
		pass

	# time.sleep(1)


# p2 : r1 d s2 e
elif curr_host == 2:
	print("ASRIEL:",nodes)

	# r1
	thisListener.recieveMsg()

	# d
	thisnode.localEvent()

	# s2 (p2) -> r2 (p1)
	target = nodes[1+1]
	try:
		thisnode.send(target.getID(), target.getHost(), target.getPort())
	except socket.error as e:
		pass
	# e
	thisnode.localEvent()

