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
    id = obj['id']
    type = obj['type']
    client = None
    bank = None

    if type == 'client':
        # create client instance
        client = Client(int(id), obj['events'])

        # set the client process to ready
        readyQueue[client.id - 1] = Global.READY

        # wait unitl all the other processes are ready
        Global.waitWorker(Global.READY, readyQueue)

        # create a stub for client
        client.createStub()

        # execute all the events
        client.executeEvents()

    elif type == 'bank':
        balance = obj['balance']
        branches = obj['branches']

        # create a gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # create a bank instance
        bank = Bank(int(id), balance, branches)

        # extend the bank instance with the gRPC
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

    print("FINISH",id,type, bank.recvMsg if type == 'bank' else client.recvMsg)
    # print("FINISH",id,type, bank.balance if type == 'bank' else None)

if __name__ == "__main__":
    # receive a json file as an input
    with open(sys.argv[1], 'r') as f:
        jsonObj = json.load(f)

    # shared counter that checks the status of the running processes
    readyQueue = Array("i", len(jsonObj))
    branches = list()

    # store the address of the branches
    for i in range(0, len(jsonObj)):
        if jsonObj[i]['type'] == 'bank':
            branches.append(jsonObj[i]['id'])

    # iterate the json file
    for i in range(0, len(jsonObj)):
        if jsonObj[i]['type'] == 'bank':
            jsonObj[i]['branches'] = branches

        # initiate the process with the print_func and pass the arguments and the shared counter
        proc = Process(target=worker,args=(jsonObj[i],readyQueue))
        # start the function
        proc.start()
