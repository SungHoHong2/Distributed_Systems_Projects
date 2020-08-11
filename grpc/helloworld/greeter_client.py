from __future__ import print_function
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    # connect the client with the server
    with grpc.insecure_channel('localhost:50051') as channel:
        # create a client instance
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        # request to server using SayHello from Greetings service
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received(1): " + response.message)
        # request to server using SayHelloAgain from Greetings service
        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received(2): " + response.message)
        # asynchronous rpc
        tmp = stub.SayHelloAgain.future(helloworld_pb2.HelloRequest(name='you'))
        response = tmp.result()
        print("Asynchronous Greeter client received(2): " + response.message)

if __name__ == '__main__':
    run()