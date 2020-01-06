# ratelimitter

ratelimitter is a simple ratelimiting imlementation, utilizing redis as its data store.

## Build
```
$ git clone git@github.com:bazulay/ratelimitter.git
$ cd ratelimiter.git
$ docker build -t ratelimitter .
```

## Run
Runnin & testing/using the system localy is done in 3 steps
- installing/running redis
- installing/running the ratelimiter_server
- using the ratelimiter_client to access 
### run redis
```
$ docker pull redis
$ docker run -di -p 6379:6379 --name redis-server redis 
```
### run ratelimiter
#### using local docker built
```
$ docker run -di -p 46001:46001 --link redis-server:redis-server --name ratelimitter-server ratelimitter
```
#### from dockerhub
```
$ docker pull bazulay/ratelimitter
$ docker run -di -p 46001:46001 --link redis-server:redis-server --name ratelimitter-server bazulay/ratelimitter
```
### Arch
#### General

[ratelimitter_client] <---grpc---> [ratelimmiter_server] <--------->[redis]

The alogorithm used here is 'fixed window counter'. It’s a simple, memory-efficient algorithm that records the number of requests from a sender occurring in the rate limit’s time interval. The algorithm takes asvantage of Redis atomic operations. Each request would increment a Redis key that included the request’s timestamp. A given Redis key looks like this:
```
<user_id>:<cur_minute_of_current_hour>
```
This key when first initialized is given an expiration tome of 1 min.
This key holds a counter that is incremented on every request.
when a new minute starts a new key is added (and the previous one expires)

the code is very simple located at src/rate_limit_logic.py
It is very simple to add another algorithm (side by side ) and run the other algorithm by simply calling to anther function.

advantages:
- very fast
- simple

disadvantages:
- It does not protect from bursts, meaning we could have a situaton when all requests come in a burst over several seconds, and if many clients behave like that than it might pose a risk on the service 

#### The API

The API is defined in the ratelimitter.proto file
```
syntax = "proto3";

package ratelimitter;

service RateLimitService{
 rpc    ShouldRateLimit(RateLimitRequest) returns (RateLimitResponse) {}
}

message RateLimitRequest{
 string UserID = 1;
 int32  PerMinuteLimit = 2;
}

message RateLimitResponse{
 int32  CurMinuteCounter = 1;
 bool   ExceededLimit    = 2;
}
```




