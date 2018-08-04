from __future__ import print_function

import random, grpc, route_guide_pb2, route_guide_pb2_grpc

def make_route_note(message, lat, lng):
    return route_guide_pb2.RouteNote(
        message=message,
        location=route_guide_pb2.Point(lat=lat, lng=lng)
    )

def guide_route_chat(stub):
    responses = stub.RouteChat(generate_messages())
    for response in responses:
        print("Received message %s at %s" % (response.message,
                                             response.location))

def generate_messages():
    messages = [
        make_route_note("First message", 0, 0),
        make_route_note("Second message", 0, 1),
        make_route_note("Third message", 1, 0),
        make_route_note("Fourth message", 0, 0),
        make_route_note("Fifth message", 1, 0),
    ]
    for msg in messages:
        print("Sending %s at %s" % (msg.message, msg.location))
        yield msg

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        print("-------------- RouteChat --------------")
        guide_route_chat(stub)

if __name__ == '__main__':
    run()