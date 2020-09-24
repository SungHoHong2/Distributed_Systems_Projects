import json
from multiprocessing import Manager
from multiprocessing import Process, Lock
from multiprocessing import Array
import time
import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc
import sys
import Global
from Client import Client
from Bank import Bank
import collections

mutex = Lock()
# from json2xml import json2xml
# from json2xml.utils import readfromjson

def worker(obj,readyQueue,returnDict):
    # Unique Process id
    id = obj['id']
    # Set the type (Bank, Client) for the Process
    type = obj['type']
    # get the list of addresses of the branch
    branches = obj['branches']
    # Pointer for Client
    client = None
    # Pointer for Bank
    bank = None

    # if the type of the process is a Client
    if type == 'client':
        # create client instance
        client = Client(int(id), obj['events'])
        # set the client process to ready
        readyQueue[len(branches) + client.id - 1] = Global.READY
        # wait until all the other processes are ready
        Global.waitWorker(Global.READY, readyQueue)
        # create a gRPC stub for client
        client.createStub()
        # execute all the events from the input
        client.executeEvents()
        # set the client process to finish
        time.sleep(1)
        mutex.acquire(1)
        readyQueue[len(branches) + int(id)-1] = Global.FINISH
        mutex.release()

    # if the type of the process is a Bank
    elif type == 'bank':
        # get the replica of the balance of the Bank
        balance = obj['balance']
        # create a gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # create a bank instance
        bank = Bank(int(id), balance, branches)
        # extend the bank instance with the gRPC server
        example_pb2_grpc.add_RPCServicer_to_server(bank, server)
        # set the server port
        print('Starting server. Listening on port 5005'+str(id))
        server.add_insecure_port('[::]:5005'+str(id))
        # start the server
        server.start()
        # set the status of the bank process to ready
        readyQueue[int(id) - 1] = Global.READY
        # wait until all the other processes are ready
        Global.waitWorker(Global.READY, readyQueue)
        # set the bank process to finish
        time.sleep(1)
        mutex.acquire(1)
        readyQueue[int(id)-1] = Global.FINISH
        mutex.release()

    # wait until all the other processes are finished
    Global.waitWorker(Global.FINISH, readyQueue)
    # print function used for debugging purposes
    # print("DEBUG",id,type, bank.recvMsg if type == 'bank' else client.recvMsg)
    # print("DEBUG",id, client.recvMsg if type == 'client' else bank.balance)
    if type == 'bank':
        time.sleep(1)
        returnDict[id] = bank.recvMsg
    if type == 'client':
        time.sleep(1)
        returnDict[len(branches)+id] = client.recvMsg

if __name__ == "__main__":
    # receive a json file as an input
    with open(sys.argv[1], 'r') as f:
        jsonObj = json.load(f)

    # set up the shared hashmap for output
    manager = Manager()
    returnDict = manager.dict()

    # shared counter that checks the status of the running processes
    readyQueue = Array("i", len(jsonObj))

    # get the process ID of the branches
    branches = list()
    for i in range(0, len(jsonObj)):
        if jsonObj[i]['type'] == 'bank':
            branches.append(jsonObj[i]['id'])

    # iterate the json file
    for i in range(0, len(jsonObj)):
        # create the Bank process
        if jsonObj[i]['type'] == 'bank':
            jsonObj[i]['branches'] = branches
            proc = Process(target=worker, args=(jsonObj[i], readyQueue, returnDict))
        # create the Client process
        elif jsonObj[i]['type'] == 'client':
            jsonObj[i]['branches'] = branches
            proc = Process(target=worker, args=(jsonObj[i], readyQueue, returnDict))
        # initiate the process
        proc.start()

    # wait until the all the output from the clients are collected
    rtnArray = list()
    hashmap = collections.defaultdict(list)
    while True:
        time.sleep(1)
        if len(returnDict.items()) == len(jsonObj):
            for key in returnDict:
                for events in returnDict[key]:
                    hashmap[events['id']].append(events)

                if returnDict[key]:
                    print({'pid' : key, 'data' : returnDict[key]})
                    rtnArray.append({'pid' : key, 'data' : returnDict[key]})
            break


    # iterate the events according to id
    idSorted = collections.defaultdict(list)
    for id,events in hashmap.items():
        # sort the events according to id
        # print(id,events)
        temp = [(event['clock'],event['name']) for event in events]
        temp = sorted(temp, key=lambda x: x[0])
        print({'eventid':id, 'data':[{'clock':item[0],'name':item[1]} for item in temp ]})
        rtnArray.append({'eventid':id, 'data':[{'clock':item[0],'name':item[1]} for item in temp ]})


    # write the output file
    filename = sys.argv[1].split('.')[0]
    with open(filename+"_output.json", "w") as outfile:
        json.dump(rtnArray,outfile,indent=2)
