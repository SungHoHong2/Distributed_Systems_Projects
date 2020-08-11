from concurrent import futures
import grpc
# a service defined by helloword.proto
import helloworld_pb2
import helloworld_pb2_grpc

# extending the service for the server
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    # when the client requests SayHello from the Greeter service
    def SayHello(self, request, context):
        # response to the client using hello HelloReply message
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
    # when the client requests SayHelloAgain from the Greeter service
    def SayHelloAgain(self, request, context):
        # response to the client using hello HelloReply message
        return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)

def run():
    # create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add class Greeter to the server
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # set the port
    server.add_insecure_port('[::]:50051')
    # A new thread will be instantiated to handle requests
    server.start()
    # cleanly block the calling thread until the server terminates
    server.wait_for_termination()

if __name__ == '__main__':
    run()