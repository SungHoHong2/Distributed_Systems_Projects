
Messages are received from dataReceived(self, data) which receives the message, 
processes it appropriately and forwards it to totalOrder (self, msg) where the fully ordered is implemented multicast.


### def totalOrder(self, msg)
This is where the fully ordered multichannel is implemented. When it gets a message from dataReceived. 
Initially the process rolls changes through 
this relationship self.clock = max (int (msg.clock),
int (self.clock)) + 1 which means it will get the maximum value between the roles
it currently has and the message rolls and posts will increase by 1.
  
Then we create a 2 value id (the creator id and its clock the creator of the message). 
Then I see if this id exists on the acks table and if not, enter it with the message, 
and if so this id already exists and the message is ack then add it to self.acks [id] 
so if it's not ack i put it in self.acks [id].
Then with another if I check if the message is NOT ack and then do it push on my queue.

In another if I check if I have received 3 acks. 2 of the other processes and 1 of 
the process informally sends the process itself. If they are acks ==3 
Then mark the message as ready. And I'm deleting self.acks [id]. 
Finally I make a temporary copy of the message I received and NOT is ack and the sender
 ID is different from the process id marks the message as ack and makes it multicast.


### def loop(self) 
This function generates a message every 2 ”for 20 times and through it
sendUpdate makes it multicast. Also after each shipment she calls
deliverMessage which checks if there is any export message and
if available export it


### def deliverMessage(self)
This function if the queue has middle elements, pops the 1st element
and if it is branded as ready then returns it to the one who made it
call it, otherwise it restores it to the queue.