import example_pb2
import example_pb2_grpc

balance = 0

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



class Bank:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
