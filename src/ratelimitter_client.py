import grpc
import ratelimitter_pb2
import ratelimitter_pb2_grpc


class RateLimitterClient(object):
    """
    Client for accessing the gRPC functionality
    """

    def __init__(self, server_host='localhost', server_port=46001):
        # configure the host and the
        # the port to which the client should connect
        # to.
        self._server_host = server_host
        self._server_port = server_port

        # instantiate a communication channel
        self._channel = grpc.insecure_channel(
            '{}:{}'.format(self._server_host, self._server_port))

        # bind the client to the server channel
        self.stub = ratelimitter_pb2_grpc.RateLimitServiceStub(self._channel)

    def should_rate_limit(self, userid, per_minute_limit=500):
        """
        Client function to call the rpc for ShouldRateLimit
        """
        rate_limit_request = ratelimitter_pb2.RateLimitRequest(
            UserID=userid,
            PerMinuteLimit=per_minute_limit)
        return self.stub.ShouldRateLimit(rate_limit_request)

