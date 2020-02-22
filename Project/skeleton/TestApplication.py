import json
from multiprocessing import Process
from multiprocessing import Array
import time
import server
import client


def print_func(obj, totalQueue, readyQueue):
    # print('Execute Process : ', arg1)
    # print(obj['name'][1:])
    # print(obj['type'])
    # print(obj['events'])

    # each process runs the server as a thread
    id = obj['name'][1:]
    server.listen(id)

    # each process keeps a dependency link
    dplink = {}

    # need to wait until all processes are ready
    readyQueue[int(id)-1] = 1
    while(len(readyQueue) != totalQueue):
        time.sleep(1)

    # generate the events
    for i in range(0, len(obj['events'])):
        print(obj['name'], obj['events'][i])
        time.sleep(1)

        # each process sends runs the event as long as the dependencies are met
        # sending ones can send to the client
    # print(readyQueue[:], len(readyQueue))


    pass





if __name__ == "__main__":

    # receive a format of input
    with open('input.json', 'r') as f:
        jsonObj = json.load(f)

    # shared variable
    readyQueue = Array("i", len(jsonObj))
    totalQueue = len(jsonObj)

    # receive the input.json
    for i in range(0, len(jsonObj)):
        print(jsonObj[i])
        # print(jsonObj[i]['name'])
        proc = Process(target=print_func, args=(jsonObj[i],totalQueue, readyQueue))
        proc.start()

    # since server.start() will not block, a sleep-loop is added to keep alive
    while True:
        time.sleep(86400)


# FIXME:

# each process should be able to communicate with each other

# each processes should be able to return the results ...

# the results will indicate how many have events they have received

# the result of the output should be wrong without the logical clock




