# ratelimitter

ratelimitter is a simple ratelimiting imlementation, utilizing redis as its data store.

## Arch

[ratelimitter_client] <---grpc---> [ratelimmiter_server] <--------->[redis]

## Build
```
$ git clone git@github.com:bazulay/ratelimitter.git
$ cd ratelimiter.git
$ 

## Run
Runnin & testing/using the system localy is done in 3 steps
- installing/running redis
- installing/running the ratelimiter_server
- using the ratelimiter_client to access 
### redis
```
$ docker pull redis
$ docker run -di -p 6379:6379 --name redis-server redis 
```
### ratelimiter
#### from code
```
$ docker build -t ratelimitter .
$ docker run -di -p 46001:46001 --link redis-server:redis-server --name ratelimitter-server ratelimitter
```
#### from dockerhub
