### Implementation of Lamport Clock

```
# run the program in this order
# the prototype has a socker error issue when the processes are not running in the correct order 
python lamport.py hosts.txt 2
python lamport.py hosts.txt 1
python lamport.py hosts.txt 0 
```

1 Code and design My implementation of Lamport Clocks consists of following Python (v. 2.7) files:
    - `lamport.py` The main class, containing main program logic. It checks, that the parameters are sufficient, reads the host file and parses it, then sleeps to wait, that all the nodes are ”online” before executing. The main event loop iterates over 100 events (local, sending, receiving), before finishing.
• lnode.py: The class LNode implements a node’s functionality. The node has functions for local events and sending. It creates an instance of a LListener class, that handles receiving messages.

• llistener.py: The LListener class has it’s own thread for handling incoming messages.

• lclock.py: The LListener and LNode share a Lamport Clock, implemented in class LClock. It has a lock to prevent both threads trying to access the same resource (clock value) at the same time.

• eventcounter.py: The EventCounter keeps track of events. Because re- ceiving messages happens on it’s own thread, the EventCounter is shared as well as the LClock. Therefore it also implements threading.Lock.

The host list is saved to a dictionary to handle possibly missing numbers and unordered nodes. The indexing is assumed to begin from 0 (and documented here). After reading hosts and separating the running host (this host) from the dictionary, the program waits for 10 seconds.

The Lamport Clock algorithm I have implemented as follows:

• local event: increment local clock by a random value from 1 to 5

• send event: increment local clock by one, send msg (containing sender ID and clock value)

• receive event: increment local clock by one, compare this and received clock value, take maximum of these and add one

Using the threading.Lock probably wasn’t the best choice to handle concur- rency, but as it wasn’t necessary to even have a separate thread for listening, I consider my solution quite adequate.

Running the code

I ran my code as follows: I started three terminals.

• 1st terminal:  python lamport.py hosts.txt 0 • 2nd terminal: python lamport.py hosts.txt 1 • 3rd terminal: python lamport.py hosts.txt 2

The program waits for socket timeouts at the end for 10 seconds, so it isnt’t ”freezed”.




