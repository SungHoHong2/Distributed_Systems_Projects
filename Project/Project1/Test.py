import json
from multiprocessing import Manager
from multiprocessing import Process
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
        readyQueue[len(branches) + int(id)-1] = Global.FINISH

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
        readyQueue[int(id)-1] = Global.FINISH

    # wait until all the other processes are finished
    Global.waitWorker(Global.FINISH, readyQueue)
    # print function used for debugging purposes
    # print("DEBUG",id,type, bank.recvMsg if type == 'bank' else client.recvMsg)
    # print("DEBUG",id, client.recvMsg if type == 'client' else bank.balance)
    if type == 'client':
        time.sleep(1)
        returnDict[id] = client.recvMsg


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
    while True:
        time.sleep(1)
        if len(returnDict.items()) == len(branches):

            for key in returnDict:
                print({'id' : key, 'recv' : returnDict[key]})
                rtnArray.append({'id' : key, 'recv' : returnDict[key]})
            break

    # write the output file
    filename = sys.argv[1].split('.')[0]
    with open(filename+"_ouput.json", "w") as outfile:
        json.dump(rtnArray,outfile)
