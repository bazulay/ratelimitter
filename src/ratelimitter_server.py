import grpc
import time
import ratelimitter_pb2
import ratelimitter_pb2_grpc
from rate_limit_logic import RateLimitLogic
from concurrent import futures


class RateLimitServiceServicer(ratelimitter_pb2_grpc.RateLimitServiceServicer):
    """
    gRPC server for RateLimit Service
    """

    def __init__(self, port=46001, redis_host='redis-server', redis_port=6379):
        self._server_port = port
        self._redis_host = redis_host
        self._redis_port = redis_port
        self._rll = RateLimitLogic(self._redis_host, self._redis_port)

    def ShouldRateLimit(self, request, context):
        """
        Implementation of the rpc ShouldRateLimit declared in the proto
        file above.
        """
        # get the UserID from the incoming request
        userid = request.UserID
        per_minute_limit = request.PerMinuteLimit
        print("userid = {}, per_minute_limit = {}".format(userid, per_minute_limit))
        cur_minute_counter = self._rll.get_user_per_minute_expiring_counter(userid)
        exceeded_limit = False
        if cur_minute_counter > per_minute_limit:
            exceeded_limit = True
        result = {'CurMinuteCounter': cur_minute_counter, 'ExceededLimit': exceeded_limit}

        return ratelimitter_pb2.RateLimitResponse(**result)

    def start_server(self):
        """
        Function which actually starts the gRPC server, and preps
        it for serving incoming connections
        """
        # declare a server object with desired number
        # of thread pool workers.
        ratelimitter_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # This line can be ignored
        ratelimitter_pb2_grpc.add_RateLimitServiceServicer_to_server(RateLimitServiceServicer(), ratelimitter_server)

        # bind the server to the port defined above
        ratelimitter_server.add_insecure_port('[::]:{}'.format(self._server_port))

        # start the server
        ratelimitter_server.start()
        print('RateLimit Server running ...')

        try:
            # need an infinite loop since the above
            # code is non blocking, and if I don't do this
            # the program will exit
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            ratelimitter_server.stop(0)
            print('RateLimit Server Stopped ...')


curr_server = RateLimitServiceServicer()
curr_server.start_server()
