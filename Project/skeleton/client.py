import grpc

# import the generated classes
import skeleton_pb2
import skeleton_pb2_grpc

def sendMsg(arg):
    print("sendMSg",arg)

    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = skeleton_pb2_grpc.SkeletonStub(channel)

    # create a valid request message
    event = skeleton_pb2.Events(id=1,name="test",dependency="test2",localclock=1)
    # make the call
    response = stub.SendMsg(event)
