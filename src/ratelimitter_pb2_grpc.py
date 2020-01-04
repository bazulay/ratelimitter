# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import ratelimitter_pb2 as ratelimitter__pb2


class RateLimitServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ShouldRateLimit = channel.unary_unary(
        '/ratelimitter.RateLimitService/ShouldRateLimit',
        request_serializer=ratelimitter__pb2.RateLimitRequest.SerializeToString,
        response_deserializer=ratelimitter__pb2.RateLimitResponse.FromString,
        )


class RateLimitServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ShouldRateLimit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RateLimitServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ShouldRateLimit': grpc.unary_unary_rpc_method_handler(
          servicer.ShouldRateLimit,
          request_deserializer=ratelimitter__pb2.RateLimitRequest.FromString,
          response_serializer=ratelimitter__pb2.RateLimitResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ratelimitter.RateLimitService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
