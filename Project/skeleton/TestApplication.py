import json
from multiprocessing import Process
from multiprocessing import Array
import time
import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc

# dictionary for dependencies
dpdict = {
    'query_request' : None,
    'query_receive' : 'query_request',
    'query_execute' : None,
    'query_reply': None,
    'query_return':'query_reply',
    'deposit_request': None,
    'deposit_receive': 'deposit_request',
    'deposit_execute': None,
    'deposit_reply': None,
    'deposit_return': 'deposit_reply',
    'withdraw_request': None,
    'withdraw_receive': 'withdraw_request',
    'withdraw_execute': None,
    'withdraw_reply': None,
    'withdraw_return': 'withdraw_reply',
    'query': ['query_request','query_receive','query_execute','query_reply','query_return'],
    'deposit':['deposit_request','deposit_receive','deposit_execute','deposit_reply','deposit_return'],
    'withdraw':['withdraw_request','withdraw_receive','withdraw_execute','withdraw_reply','withdraw_return'],
}

# each process keeps a dependency link
dplink = []

# result generated as a output file
eventList = []

class ExampleServicer(example_pb2_grpc.ExampleServicer):

    def StrName(self,request, context):
        response = example_pb2.Event()
        eventRecord = {
            'id' : request.id,
            'name' : request.name,
            'localclock' : request.localclock
        }
        # store the received request to the dependencies
        dplink.append(eventRecord)
        return response

def print_func(obj,readyQueue):
    localClock = 0
    # print(obj['name'][1:])
    # print(obj['type'])
    # print(obj['events'])

    # each process runs the server as a thread
    id = obj['name'][1:]

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServicer_to_server(ExampleServicer(), server)

    # listen on port 50051
    print('Starting server. Listening on port 5005'+str(id))
    server.add_insecure_port('[::]:5005'+str(id))
    server.start()

    # need to wait until all processes are ready
    readyQueue[int(id)-1] = 1
    while(True):
        allSet = True
        for i in range(0, len(readyQueue)):
            if readyQueue[i] != 1:
                allSet = False

        if allSet == True:
            break

    # generate the events
    for i in range(0, len(obj['events'])):
        # print(obj['name'], obj['events'][i])
        arg = obj['events'][i]
        # print('[FRISK]', arg)

        # check if dependency exists
        if dpdict[arg['name']]:
            # if exists
            linkExists = False
            while(True):
                time.sleep(0.5)
                for s in range(0, len(dplink)):
                    if dplink[s]['id'] == arg['id'] and dplink[s]['name'] == dpdict[arg['name']]:
                        # proceed
                        # if id == '1':
                            # print(arg['name'],"dependency found")
                            # local clock from remote process
                            # print(dplink[s]['localclock'])

                        linkExists = True
                        break

                if linkExists:
                    break

        eventList.append({'id':arg['id'],
                          'name':arg['name'],
                          'localClock':localClock})

        if 'dest' in arg:
            # each process runs the event as long as the dependencies are met
            channel = grpc.insecure_channel('localhost:5005'+str(arg['dest']))
            # create a stub (client)
            stub = example_pb2_grpc.ExampleStub(channel)
            event = example_pb2.Event(id=arg['id'],name=arg['name'],localclock=localClock)
            stub.StrName(event)

        localClock += 1

    with open(obj['name']+'.json', 'w+') as outfile:
        json.dump(eventList, outfile)

    # set the status to finish
    readyQueue[int(id)-1] = 2

    # print out all the dependency link
    # print(obj['name'], dplink)

    # print out all the invoked events
    # for s in eventList:
    #     print(s)


if __name__ == "__main__":

    # receive a format of input
    with open('input.json', 'r') as f:
        jsonObj = json.load(f)

    # shared variable
    readyQueue = Array("i", len(jsonObj))

    # receive the input.json
    for i in range(0, len(jsonObj)):
        # print(jsonObj[i])
        # print(jsonObj[i]['name'])
        proc = Process(target=print_func,args=(jsonObj[i],readyQueue))
        proc.start()


    # check the readyQueue and see whether all the processes are finished
    while(True):
        time.sleep(1)
        allSet = True
        for i in range(0, len(readyQueue)):
            if readyQueue[i] != 2:
                allSet = False

        if allSet == True:
            break

    print("all processes are finished")

    # read all the files
    result = {}

    for obj in jsonObj:
        print(obj['name'])

        with open(obj['name']+'.json', 'r') as f:
            chkObj = json.load(f)
            for item in chkObj:
                if item['id'] not in result:
                    result[item['id']] = {}
                    result[item['id']][item['name']] = item['localClock']
                else:
                    result[item['id']][item['name']] = item['localClock']

    for key,value in result.items():
        print(key,value)

