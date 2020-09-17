import grpc
import example_pb2
import example_pb2_grpc
import time

class Client:
    def __init__(self, id, events):
        # unique ID of the Client
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        # local clock
        self.clock = 0

    def createStub(self):
        # set the address to the branch (processID of the Client + 1)
        channel = grpc.insecure_channel('localhost:5005' + str(self.id))
        # create the stub for the Client
        stub = example_pb2_grpc.RPCStub(channel)
        # set the stub to the pointer
        self.stub = stub

    def executeEvents(self):
        # iterate the events
        for event in self.events:
            #TODO: Event_Request
            self.clock += 1
            self.recvMsg.append({'id': event['id'], 'name': event['interface']+'_request', 'clock' : self.clock })

            # if the event is query
            if event['interface'] == 'query':
                # sleep a while to guarantee complete propagation
                time.sleep(3)
                # request for the total balance of the bank
                msg = example_pb2.Event(id=event['id'], interface=event['interface'],clock=self.clock)
            # if the event is withdraw or deposit
            elif event['interface'] == 'withdraw' or event['interface'] == 'deposit':
                # submit the update request to the branch
                msg = example_pb2.Event(id=event['id'], interface=event['interface'],money= event['money'],clock=self.clock)
            # send message to the server
            response = self.stub.MsgDelivery(msg)
            # record the success response from the server
            rtnObj = { 'interface' : response.interface,
                       'result':response.result }
            if response.interface == 'query':
                rtnObj['money'] = response.money

            #TODO: Event_Return
            # self.clock += 1
            self.clock = max(self.clock, response.clock) + 1
            self.recvMsg.append({'id': response.id, 'name': response.interface+'_return', 'clock' : self.clock })
