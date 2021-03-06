# Lamport Logical Clock

### Logical Clocks
In a distributed system, with multiple processes, where events can occur in any order, it is difficult to maintain a global clock synchronously for each process.
<br>Logical clocks allow the processes to order their events (calculations, logic etc), with respect to other events, and thus allows to maintain the causal order between events.


### Lamport Logical Clock
An algorithm, developed by Leslie Lamport, to find the logical clock of an event in a distributed system.

Types of events that can occur -
1) Local - A normal execution within a process
2) Send - A process sends a message to another process
3) Receive - A process receives a message sent by another process

RULES

* If a and b are events in process P~, and a comes
before b, then C<sub>i</sub>(a) < C<sub>i</sub>(b).

* If a is the sending of a message by process Pi
and b is the receipt of that message by process P<sub>i</sub>, then
C<sub>i</sub>(a) < C<sub>i</sub>(b)..


### Algorithm to calculate Lamport Logical Clock
Let ​ a ​ be some event encountered by P.
1. If ​ a ​ is the first event and is an internal or send event, then LC(​ a ​ ) = 1.
2. If ​ a ​ is the first event and is a receive event, then LC(​ a ​ ) = ​ k ​ + 1 where​ k ​ is the LC-value of the send
event corresponding to ​ a ​ (that has occurred at a process other than P).
3. If ​ a ​ is not the first event and is an internal or send event, then LC(​ a ​ ) = ​ k ​ + 1 where ​ k ​ is the LC-value of
the event just before ​ a ​ at process P.
4. If ​ a ​ is not the first event and is a receive event, let ​ b ​ be the send event corresponding to ​ a ​ (that has
occurred at a process other than P) and ​ k ​ be the clock value of the event just before ​ a ​ at process P. Then
LC(a) = max{ k, LC(b) } + 1


### Implementation
Given a set of events occuring at various processes, calculate the logical clocks for each event.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example - 
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p0 : a s1 r3 b
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p1 : c r2 s3
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p2 : r1 d s2 e

<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Expected Output -
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p0 : 1 2 8 9
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p1 : 1 6 7
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;p2 : 3 4 5 6