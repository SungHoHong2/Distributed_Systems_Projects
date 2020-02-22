import grpc
import skeleton_pb2
import skeleton_pb2_grpc

def runEvent(arg):

    # the event needs to be sent to the external process
    if 'dest' in arg:

        print('before sending', arg['dest'])
        # open a gRPC channel
        channel = grpc.insecure_channel('localhost:5005'+str(arg['dest']))

        # create a stub (client)
        stub = skeleton_pb2_grpc.SkeletonStub(channel)

        # create a valid request message
        event = skeleton_pb2.Events(id=1,name="test",dependency="test2",localclock=1)
        # make the call
        response = stub.SendMsg(event)
        print('msgSent', response)

