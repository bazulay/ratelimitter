import argparse
from datetime import datetime
import pprint
from ratelimitter_client import RateLimitterClient
from string import ascii_lowercase
import time


DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
rls = None
users_results = {}
users = []


def print_user_results():
    pprint.pprint(users_results, width=1)


def test_system(per_min_limit=500, iterations=100000000, delay=0.0):
    global users_results
    # the below 2 lines produce a list of users in the format aaaa,bbbb...zzzz
    for c in ascii_lowercase:
        users.append(c*4)
    start = datetime.now()
    prev_moh = -1
    for itr in range(iterations):
        user = users[itr%26]
        moh = time.gmtime(time.time()).tm_min
        user_minute_counter_name = "{}:{}".format(user, moh)
        response = rls.should_rate_limit(user, per_min_limit)
        if not response.ExceededLimit:
            try:
                users_results[user_minute_counter_name] += 1
            except KeyError:
                if moh != prev_moh:
                    print_user_results()
                    prev_moh = moh
                users_results[user_minute_counter_name] = 1
        if delay > 0:
            time.sleep(delay)
    end = datetime.now()
    print("############################################")
    print("################## summary #################")
    print("############################################")
    print_user_results()
    delta = end - start
    print("started at: {}".format(start.strftime(DATETIME_FMT)))
    print("ended   at: {}".format(end.strftime(DATETIME_FMT)))
    print("Total Seconds: {}".format(delta.total_seconds()))



def main():
    global rls
    parser_description = "Test rate limit system"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument('--host', type=str, default='localhost', nargs='?',
                        help='the ratelimitter server to connect to')
    parser.add_argument('--port', type=int, default=46001, nargs='?',
                        help='the ratelimitter server port to connect to')
    parser.add_argument('--pml', type=int, default=500, nargs='?',
                        help='the per minute limit')
    parser.add_argument('--itr', type=int, default=10000, nargs='?',
                        help='the total amount of requests to the ratelimitter')
    parser.add_argument('--delay', type=float, default=0.0, nargs='?',
                        help='delay to perform between calls (default = 0.0)')

    args = parser.parse_args()
    rls = RateLimitterClient(args.host, args.port)
    test_system(args.pml, args.itr, args.delay)


if __name__ == '__main__':
    main()
