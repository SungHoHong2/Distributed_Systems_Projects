import grpc
import example_pb2
import example_pb2_grpc

class Bank(example_pb2_grpc.RPCServicer):

    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()
        self.recvMsg = list()
        for addr in self.branches:
            if addr != self.id :
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
        self.recvMsg.append(eventRecord)

        if request.interface == 'query':
            pass

        elif request.interface == 'deposit':
            self.balance += request.money
            # broadcast
            for stub in self.stubList:
                msg = example_pb2.Event(interface=request.interface+"_broadcast", money=request.money)
                stub.MsgDelivery(msg)

        elif request.interface == 'withdraw':
            self.balance -= request.money
            # broadcast
            for stub in self.stubList:
                msg = example_pb2.Event(interface=request.interface+"_broadcast", money=request.money)
                stub.MsgDelivery(msg)

        elif request.interface == 'deposit_broadcast':
            self.balance += request.money

        elif request.interface == 'withdraw_broadcast':
            self.balance -= request.money

        # return success to the client
        response = example_pb2.Event(interface= request.interface + "_success!", money=request.money)
        return response