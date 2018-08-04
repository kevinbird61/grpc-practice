from concurrent import futures
import time
import math

import grpc

import route_guide_pb2
import route_guide_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""
    def RouteChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            yield new_note
            #for prev_note in prev_notes:
            #   if prev_note.location == new_note.location:
            #        yield prev_note
            # prev_notes.append(new_note)

if __name__ == '__main__':
    serve()