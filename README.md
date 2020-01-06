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

The alogorithm used here is 'fixed window counter'. It’s a simple, memory-efficient algorithm that records the number of requests from a sender occurring in the rate limit’s time interval (one minute). The algorithm takes advantage of Redis atomic operations. Each request would increment a Redis key that included the request’s minute-of-the-hour (extracted from current timestamp). A given Redis key looks like this:
```
<user_id>:<cur_minute_of_current_hour>
```
This key when first initialized is given an expiration time of 1 min.
This key holds a counter that is incremented on every request.
when a new minute starts a new key is added (and the previous one expires)

the code is very simple located at src/rate_limit_logic.py
It is very simple to add another algorithm (side by side ) and run the other algorithm by simply calling to another function.

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
### Rinning the test

I wrote a simple test that checks this logic (located at src/test_ratelimitter.py)
This simple test has some commandline flags that enable tuning.
```
$ python test_ratelimitter.py --help
usage: test_ratelimitter.py [-h] [--host [HOST]] [--port [PORT]] [--pml [PML]]
                            [--itr [ITR]] [--delay [DELAY]]

Test rate limit system

optional arguments:
  -h, --help       show this help message and exit
  --host [HOST]    the ratelimitter server to connect to
  --port [PORT]    the ratelimitter server port to connect to
  --pml [PML]      the per minute limit
  --itr [ITR]      the total amount of requests to the ratelimitter
  --delay [DELAY]  delay to perform between calls (default = 0.0)

```
This test simply simulates 26 users (aaaa ... zzzz) and iterates through them and sends requests,
eventually one can see whether any of them passed the per-minute-limit

You canrun it in 2 ways

#### from within the ratelimitter running container
```
docker exec -ti <container_id> /bin/sh
cd src
python test_ratelimitter.py
```
#### from outside the ratelimitter
for that you'll need a virtualenv containing the packages in the requirements.txt file (at the root of the repo)
use the command line flags to direct
and than you can simply

```
python test_ratelimitter.py
```



