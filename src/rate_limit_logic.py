import redis
import time


class RateLimitLogic:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        # not handling the potential exception in the call below,
        # because we need immediate indication when the server is not reachable
        self._rds = redis.Redis(host, port)

    def __del__(self):
        if self._rds:
            self._rds.close()

    def get_user_per_minute_expiring_counter(self, userid):
        # moh is the current minute of the current hour
        moh = time.gmtime(time.time()).tm_min
        user_minute_counter_name = "{}:{}".format(userid, moh)
        # print("user_minute_counter_name = {}".format(user_minute_counter_name))
        added_counter = self._rds.set(name=user_minute_counter_name,
                                      value=1, ex=60, nx=True)
        if added_counter:
            minute_counter = 1
        else:
            minute_counter = self._rds.incr(user_minute_counter_name)
        # print("minute_counter = {}, type(minute_counter) = {}".format(minute_counter,
        #      type(minute_counter)))
        return minute_counter
