import json
from multiprocessing import Process
from multiprocessing import Array
import time
import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc
import sys

# dictionary for dependencies
dpdict = {
    'query_receive'     :   'query_request',
    'query_execute'     :   'query_receive',
    'query_reply'       :   'query_execute',
    'query_return'      :   'query_reply',

    'deposit_receive'   :   'deposit_request',
    'deposit_execute'   :   'deposit_receive',
    'deposit_reply'     :   'deposit_execute',
    'deposit_return'    :   'deposit_reply',

    'withdraw_receive'  :   'withdraw_request',
    'withdraw_execute'  :   'withdraw_receive',
    'withdraw_reply'    :   'withdraw_execute',
    'withdraw_return'   :   'withdraw_reply',
}
# each process keeps a private message buffers
sendMsg, execMsg, recvMsg = list(), list(), list()

# server
class ExampleServicer(example_pb2_grpc.ExampleServicer):
    def MsgDelivery(self,request, context):
        # create a fake object as returning "None" causes error
        response = example_pb2.Event()
        # received a message from external process
        eventRecord = {
            'id' : request.id,
            'name' : request.name,
            'money' : request.money
        }
        # store the received request to the buffer
        recvMsg.append(eventRecord)
        # return the fake object
        return response

def transaction(balance, event):
    if event['name'] == 'query_execute' and balance >= event['money']:
        return event['money']
    elif event['name'] == 'deposit_execute':
        return balance + event['money']
    elif event['name'] == 'withdraw_execute' and balance >= event['money']:
        return balance - event['money']
    else:
        print('wrong result detected!', event, balance)
        return -1

def worker(obj,readyQueue):
    # get the id of the process
    id = obj['name'][1:]
    # get the type of the process
    type = obj['type']
    # create a balance for bank processes
    if type == 'bank':
        balance = obj['balance']

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServicer_to_server(ExampleServicer(), server)

    # listen on port 50051
    print('Starting server. Listening on port 5005'+str(id))
    server.add_insecure_port('[::]:5005'+str(id))
    server.start()

    # need to wait until all processes are ready
    readyQueue[int(id)-1] = 1
    waitWorker(1, readyQueue)

    print(id,"Function BEGIN!")
    # generate the events
    for i in range(0, len(obj['events'])):
        # print(obj['name'], obj['events'][i])
        event = obj['events'][i]
        # print(id, event)
        # the event is sending the message to external
        if 'dest' in event:
            # get the destination
            channel = grpc.insecure_channel('localhost:5005'+str(event['dest']))
            # create a stub (client)
            stub = example_pb2_grpc.ExampleStub(channel)

            if event['name'] in dpdict:
               depFound = False
               while not(depFound):
                    time.sleep(1)
                    for i in range(len(sendMsg)):
                        if sendMsg[i]['name'] == dpdict[event['name']]:
                            msg = sendMsg.pop(i)
                            depFound = True
                            event['money'] = msg['money']
                            break
            print('FRISK',id, event)
            # craft a message
            msg = example_pb2.Event(id=event['id'],name=event['name'],money= event['money'])
            # send and receive a message
            stub.MsgDelivery(msg)

        if 'recv' in event:
            # wait for the reply function
            # print(id, event, 'waiting for ...', dpdict[event['name']])
            depFound = False
            while not(depFound):
                time.sleep(1)
                for i in range(len(recvMsg)):
                    if recvMsg[i]['name'] == dpdict[event['name']]:
                        msg = recvMsg.pop(i)
                        depFound = True
                        event['money'] = msg['money']
                        print('FRISK',id, event)
                        execMsg.append(event)
                        break

        if 'exec' in event:
            # print(id, event, 'waiting for ...', dpdict[event['name']])
            depFound = False
            while not(depFound):
                time.sleep(1)
                for i in range(len(execMsg)):
                    if execMsg[i]['name'] == dpdict[event['name']]:
                        msg = execMsg.pop(i)
                        event['money'] = msg['money']
                        print('FRISK',id, event)
                        balance = transaction(balance, event)
                        sendMsg.append(event)
                        depFound = True
                        break
            # get the money from the file

    # set the status to finish
    readyQueue[int(id)-1] = 2
    print(id,"Function END!")
    waitWorker(2, readyQueue)
    if type == 'bank':
        print(id, 'balance', balance)


def waitWorker(type, queue):
    allSet = True
    while(True):
        time.sleep(1)
        allSet = True
        for i in range(0, len(queue)):
            if queue[i] != type:
                allSet = False
        if allSet == True:
            break

if __name__ == "__main__":

    # receive a json file as an input
    with open(sys.argv[1], 'r') as f:
        jsonObj = json.load(f)

    # shared counter that is used for counting the running processes
    readyQueue = Array("i", len(jsonObj))

    # iterate the json file
    for i in range(0, len(jsonObj)):
        # initiate the process with the print_func and pass the arguements and the shared counter
        proc = Process(target=worker,args=(jsonObj[i],readyQueue))
        # start the function
        proc.start()

    # check the shared counter and see whether all the processes are finished
    waitWorker(2, readyQueue)
    print("[Test]:all processes are finished")