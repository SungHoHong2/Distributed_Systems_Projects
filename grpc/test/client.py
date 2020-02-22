import grpc

# import the generated classes
import calculator_pb2
import calculator_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = calculator_pb2_grpc.CalculatorStub(channel)

# create a valid request message
number = calculator_pb2.Number(value=16)
# make the call
response = stub.SquareRoot(number)

print(response.value)

hello = calculator_pb2.HelloRequest(greeting="hello")
response = stub.StrName(hello)
print(response)