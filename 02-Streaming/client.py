from __future__ import print_function

import json, random, grpc, route_guide_pb2, route_guide_pb2_grpc


def read_route_guide_database():
    """Reads the route guide database.
    Returns:
        The full contents of the route guide database as a sequence of
        route_guide_pb2.Features.
    """
    feature_list = []
    with open("route_guide_db.json") as route_guide_db_file:
        for item in json.load(route_guide_db_file):
            feature = route_guide_pb2.Feature(
                name=item["name"],
                location=route_guide_pb2.Point(
                    lat=item["location"]["latitude"],
                    lng=item["location"]["longitude"]))
            feature_list.append(feature)
    return feature_list

def make_route_note(message, lat, lng):
    return route_guide_pb2.RouteNote(
        message=message,
        location=route_guide_pb2.Point(lat=lat, lng=lng)
    )

# normal (one parameter, one return value)
def guide_get_one_feature(stub, point):
    feature = stub.GetFeature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return 
    if feature.name:
        print("Feature called %s at %s" % (feature.name, feature.location))
    else:
        print("Found no feature at %s" % feature.location)


def guide_get_feature(stub):
    # using 2 point
    guide_get_one_feature(stub, route_guide_pb2.Point(lat=409146138,lng=-746188906))
    guide_get_one_feature(stub, route_guide_pb2.Point(lat=0, lng=0))

def guide_list_features(stub):
    rectangle = route_guide_pb2.Rectangle(
        lo=route_guide_pb2.Point(lat=400000000, lng=-750000000),
        hi=route_guide_pb2.Point(lat=420000000, lng=-730000000))
    print("Looking for features between 40, -75 and 42, -73")

    # server-to-client
    features = stub.ListFeatures(rectangle)

    for feature in features:
        print("Feature called %s at %s" % (feature.name, feature.location))

def generate_route(feature_list):
    for _ in range(0, 10):
        random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
        print("Visiting point %s" % random_feature.location)
        yield random_feature.location

# client-to-server
def guide_record_route(stub):
    feature_list = read_route_guide_database()

    route_iterator = generate_route(feature_list)
    route_summary = stub.RecordRoute(route_iterator)
    print("Finished trip with %s points " % route_summary.point_count)
    print("Passed %s features " % route_summary.feature_count)
    print("Travelled %s meters " % route_summary.distance)
    print("It took %s seconds " % route_summary.elapsed_time)

# bidirectional 
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
        print("-------------- GetFeature --------------")
        guide_get_feature(stub)
        print("-------------- ListFeatures --------------")
        guide_list_features(stub)
        print("-------------- RecordRoute --------------")
        guide_record_route(stub)
        print("-------------- RouteChat --------------")
        guide_route_chat(stub)

if __name__ == '__main__':
    run()