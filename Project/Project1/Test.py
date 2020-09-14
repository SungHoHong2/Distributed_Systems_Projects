import json
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

def worker(obj,readyQueue):
    # Unique Process id
    id = obj['id']
    # Set the type (Bank, Client) for the Process
    type = obj['type']
    # Pointer for Client
    client = None
    # Pointer for Bank
    bank = None

    # if the type of the process is a Client
    if type == 'client':
        # create client instance
        client = Client(int(id), obj['events'])
        # set the client process to ready
        readyQueue[client.id - 1] = Global.READY
        # wait until all the other processes are ready
        Global.waitWorker(Global.READY, readyQueue)
        # create a gRPC stub for client
        client.createStub()
        # execute all the events from the input
        client.executeEvents()

    # if the type of the process is a Bank
    elif type == 'bank':
        # get the replica of the balance of the Bank
        balance = obj['balance']
        # get the unique ID of its peer branches
        branches = obj['branches']
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

    time.sleep(1)
    # set the process to finish
    readyQueue[int(id)-1] = Global.FINISH
    # wait until all the other processes are finished
    Global.waitWorker(Global.FINISH, readyQueue)
    # print function used for debugging purposes
    # print("DEBUG",id,type, bank.recvMsg if type == 'bank' else client.recvMsg)
    # print function for checking the consistency of the replica
    print("FINISH",id,type, bank.balance if type == 'bank' else None)

if __name__ == "__main__":
    # receive a json file as an input
    with open(sys.argv[1], 'r') as f:
        jsonObj = json.load(f)

    # shared counter that checks the status of the running processes
    readyQueue = Array("i", len(jsonObj))

    # get the process ID of the branches
    branches = list()
    for i in range(0, len(jsonObj)):
        if jsonObj[i]['type'] == 'bank':
            branches.append(jsonObj[i]['id'])

    # iterate the json file
    for i in range(0, len(jsonObj)):
        # give the list of the processID of branches to the Bank process
        if jsonObj[i]['type'] == 'bank':
            jsonObj[i]['branches'] = branches
        # initiate the process with the print_func and pass the arguments and the shared counter
        proc = Process(target=worker,args=(jsonObj[i],readyQueue))
        # start the function
        proc.start()
