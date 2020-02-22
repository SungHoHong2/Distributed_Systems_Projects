import grpc
from concurrent import futures
import time
import skeleton_pb2
import skeleton_pb2_grpc

class SkeletonServicer(skeleton_pb2_grpc.SkeletonServicer):

    def SendMsg(self, request, context):
        response = skeleton_pb2.Events
        response.localclock = 9
        return response

def listen(arg):
    # listen on port 50051
    print('Starting server. Listening on port 5005'+str(arg))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port('[::]:5005'+str(arg))
    server.start()
