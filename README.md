# rate_limitter

docker pull redis
docker run -di -p 6379:6379 --name redis-server redis

docker run -di -p 46001:46001 --link redis-server:redis-server --name ratelimitter-server ratelimitter
