import grpc
import example_pb2
import example_pb2_grpc

class Bank(example_pb2_grpc.RPCServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Bank
        self.id = id
        # replica of the Bank's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # TODO: Students are expected to update the local clock
        # local clock
        self.clock = 0
        # iterate the processID of the branches
        for addr in self.branches:
            # if the branchID is not itself
            if addr != self.id :
                # set the address to the branch
                channel = grpc.insecure_channel('localhost:5005' + str(addr))
                # create a stub
                stub = example_pb2_grpc.RPCStub(channel)
                # append the stub to the pointer
                self.stubList.append(stub)

    # TODO: Student's implementation
    def eventRequest(self,request):
        self.clock = max(self.clock, request.clock) + 1
        self.recvMsg.append({'id': request.id, 'name': request.interface + '_request', 'clock': self.clock})

    # TODO: Student's implementation
    def eventExecute(self,request):
        self.clock += 1
        self.recvMsg.append({'id': request.id, 'name': request.interface + '_execute', 'clock': self.clock})

    # TODO: Student's implementation
    def eventResponse(self,response):
        self.clock = max(self.clock, response.clock) + 1
        self.recvMsg.append({'id': response.id, 'name': response.interface + '_response', 'clock': self.clock})


    def MsgDelivery(self,request, context):
        # record the received request
        eventRecord = {
            'interface' : request.interface,
            'money' : request.money
        }

        # if the request is a query from the Client
        if request.interface == 'query':
            # do nothing
            pass

        # if the request is a deposit from the Client
        elif request.interface == 'deposit':
            # increase the requested amount to the replica
            self.balance += request.money

            # TODO: Student's implementation
            self.eventRequest(request)
            self.eventExecute(request)

            # broadcast the update to its peers
            for stub in self.stubList:
                msg = example_pb2.Event(id=request.id, interface=request.interface+"_broadcast", money=request.money, clock=self.clock)
                response = stub.MsgDelivery(msg)

                # TODO: Student's implementation
                self.eventResponse(response)

        # if the request is a withdraw from the Client
        elif request.interface == 'withdraw':
            # decrease the requested amount to the replica
            self.balance -= request.money

            # TODO: Student's implementation
            self.eventRequest(request)
            self.eventExecute(request)

            # broadcast the update to its peers
            for stub in self.stubList:
                msg = example_pb2.Event(id=request.id, interface=request.interface+"_broadcast", money=request.money, clock=self.clock)
                response = stub.MsgDelivery(msg)

                # TODO: Student's implementation
                self.eventResponse(response)

        # if the request is a deposit broadcast from the branch
        elif request.interface == 'deposit_broadcast':
            # increase the requested amount to the replica
            self.balance += request.money

            # TODO: Student's implementation
            self.eventRequest(request)
            self.eventExecute(request)

        # if the request is a withdraw broadcast from the branch
        elif request.interface == 'withdraw_broadcast':
            # decrease the requested amount to the replica
            self.balance -= request.money

            # TODO: Student's implementation
            self.eventRequest(request)
            self.eventExecute(request)

        # return the response back to the requested Process
        response = example_pb2.Event(id=request.id,interface=request.interface,money=self.balance,clock=self.clock,result="success")
        return response