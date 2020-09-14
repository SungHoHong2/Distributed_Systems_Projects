import grpc
import example_pb2
import example_pb2_grpc

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

    # TODO: students are expected to create the Client stub
    def createStub(self):
        # set the address to the branch (processID of the Client + 1)
        channel = grpc.insecure_channel('localhost:5005' + str(self.id + 1))
        # create the stub for the Client
        stub = example_pb2_grpc.RPCStub(channel)
        # set the stub to the pointer
        self.stub = stub

    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self):
        # iterate the events
        for event in self.events:
            # print(id,event['interface'],event['money'])
            msg = example_pb2.Event(interface=event['interface'],money= event['money'])
            # send message to the server
            response = self.stub.MsgDelivery(msg)
            # record the success response from the server
            self.recvMsg.append({'interface' : response.interface,'money' : response.money})

