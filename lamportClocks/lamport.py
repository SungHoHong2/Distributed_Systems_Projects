import lnode
import random
import socket
import sys
import time
import eventcounter

# arguments [hosts.txt], [Current Node Number]
if len(sys.argv) < 2:
	print("Usage: program configuration_file line")
	sys.exit()

# get the configuration
conf_file = sys.argv[1]

hosts = open(conf_file)
nodes = {}

# init event counter
events = eventcounter.EventCounter()
# get the current node number
curr_host = int(sys.argv[2])

# get the configuration of all nodes
for idx, line in enumerate(hosts):
	l = line.split()
	if not l:
		continue

	# take correct row for this node from the conf file.
	if idx == curr_host:
		thisnode = lnode.LNode(events, int(l[0]), l[1], int(l[2]))
		continue

	nodes[int(l[0])] = lnode.LNode(events, int(l[0]), l[1], int(l[2]))

# time to start all the nodes needed, hopefully.
time.sleep(5)
thisListener = thisnode.listen()

# Connecting Nodes
# nodes[1] == 0
# # nodes[2] == 1
# # nodes[3] == 2

# p0 : a s1 r3 b
# p1 : c r2 s3
# p2 : r1 d s2 e

# p0 : a s1 r3 b
if curr_host == 0:
	# a
	# create local event
	thisnode.localEvent()

	# s1 (p0) -> r1 (p2)
	# node 0 sends message to node 2
	target = nodes[2+1]
	try:
		thisnode.send(target.getID(), target.getHost(), target.getPort())
	except socket.error as e:
		pass

	# r3
	# receive message
	thisListener.recieveMsg()

	# b
	# create local event
	thisnode.localEvent()


# p1 : c r2 s3
elif curr_host == 1:
	# c
	# create local event
	thisnode.localEvent()

	# r2
	# receive message
	thisListener.recieveMsg()

	# s3 (p1) -> r3 (p0)
	# node 1 sends message to node 0
	target = nodes[0+1]
	try:
		thisnode.send(target.getID(), target.getHost(), target.getPort())
	except socket.error as e:
		pass


# p2 : r1 d s2 e
elif curr_host == 2:
	# r1
	# receive message
	thisListener.recieveMsg()

	# d
	# create local event
	thisnode.localEvent()

	# s2 (p2) -> r2 (p1)
	# node 2 send message to node 1
	target = nodes[1+1]
	try:
		thisnode.send(target.getID(), target.getHost(), target.getPort())
	except socket.error as e:
		pass
	# e
	# create local event
	thisnode.localEvent()

