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

id = 0
balance = 0
recvMsg = list()
branchAddress = list()
client = None
bank = None

class RPC(example_pb2_grpc.RPCServicer):

    def __init__(self):
        self.stubList = list()
        for addr in branchAddress:
            if addr != id:
                channel = grpc.insecure_channel('localhost:5005' + str(addr))
                stub = example_pb2_grpc.RPCStub(channel)
                self.stubList.append(stub)

    def MsgDelivery(self,request, context):
        # record the request sent from the client
        eventRecord = {
            'interface' : request.interface,
            'money' : request.money
        }
        # print(id, eventRecord)
        recvMsg.append(eventRecord)

        global balance
        if request.interface == 'query':
            pass

        elif request.interface == 'deposit':
            balance += request.money
            # broadcast
            for stub in self.stubList:
                msg = example_pb2.Event(interface=request.interface+"_broadcast", money=request.money)
                stub.MsgDelivery(msg)

        elif request.interface == 'withdraw':
            balance -= request.money
            # broadcast
            for stub in self.stubList:
                msg = example_pb2.Event(interface=request.interface+"_broadcast", money=request.money)
                stub.MsgDelivery(msg)

        elif request.interface == 'deposit_broadcast':
            balance += request.money

        elif request.interface == 'withdraw_broadcast':
            balance -= request.money

        # return success to the client
        response = example_pb2.Event(interface= request.interface + "_success!", money=request.money)
        return response


def worker(obj,readyQueue):
    global id
    id = obj['id']
    type = obj['type']
    global client

    if type == 'client':
        # create client instance
        client = Client(int(id), obj['events'])

        # wait until all the processes are ready
        readyQueue[client.id - 1] = Global.READY
        Global.waitWorker(Global.READY, readyQueue)

        # create a stub for client
        client.createStub()

        # execute all the events
        client.executeEvents()

    elif type == 'bank':
        global balance
        balance = obj['balance']
        # create a gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        example_pb2_grpc.add_RPCServicer_to_server(RPC(), server)
        print('Starting server. Listening on port 5005'+str(id))
        server.add_insecure_port('[::]:5005'+str(id))
        server.start()

        readyQueue[int(id) - 1] = Global.READY
        Global.waitWorker(Global.READY, readyQueue)

    time.sleep(1)
    readyQueue[int(id)-1] = Global.FINISH
    Global.waitWorker(Global.FINISH, readyQueue)
    # print("FINISH",id,type,recvMsg, balance if type == 'bank' else None)
    print("FINISH",id,type, balance if type == 'bank' else None)

if __name__ == "__main__":
    # receive a json file as an input
    with open(sys.argv[1], 'r') as f:
        jsonObj = json.load(f)

    # shared counter that checks the status of the running processes
    readyQueue = Array("i", len(jsonObj))

    # store the address of the branches
    for i in range(0, len(jsonObj)):
        if jsonObj[i]['type'] == 'bank':
            branchAddress.append(jsonObj[i]['id'])

    # iterate the json file
    for i in range(0, len(jsonObj)):
        # initiate the process with the print_func and pass the arguments and the shared counter
        proc = Process(target=worker,args=(jsonObj[i],readyQueue))
        # start the function
        proc.start()
