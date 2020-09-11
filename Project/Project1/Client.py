import grpc
import example_pb2
import example_pb2_grpc

class Client:
    def __init__(self, id, events):
        self.id = id
        self.events = events
        self.recvMsg = list()
        self.stub = None

    def createStub(self):
        channel = grpc.insecure_channel('localhost:5005' + str(self.id + 1))
        stub = example_pb2_grpc.RPCStub(channel)
        self.stub = stub

    def executeEvents(self):
        for event in self.events:
            # print(id,event['interface'],event['money'])
            msg = example_pb2.Event(interface=event['interface'],money= event['money'])
            # send message to the server
            response = self.stub.MsgDelivery(msg)
            # record the success response from the server
            self.recvMsg.append({'interface' : response.interface,'money' : response.money})

