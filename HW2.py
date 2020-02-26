# AUTHOR: Brian Fogarty
import csv
import numpy as np
import redis
import time


# 0. HELPER FUNCTIONS

def load_follows(redis_cnx, filepath='./data/assignment.csv'):
    """Loads all followers relationships into Redis from the given file path."""
    follows_key = 'user:{}:follows'
    with open(filepath, 'r') as in_file:
        reader = csv.reader(in_file)
        # 1. Iterate over each row of the csv file.
        for row_id, row_val in reader:
            # 2. Clean and Redis-key-format each row's string data.
            user_id = str(row_id).replace('[', '').replace(']', '').strip()
            follows_arr = [str(f.strip()) for f in row_val.replace('[', '').replace(']', '').split(',')]
            # 3. Store the set of user_ids this user follows.
            redis_cnx.sadd(follows_key.format(user_id), *follows_arr)


def load_followed_by(redis_cnx, filepath='./data/assignment.csv'):
    """Loads all followed_by relationships into Redis from the given file path."""
    followed_by_key = 'user:{}:followedBy'
    with open(filepath, 'r') as in_file:
        reader = csv.reader(in_file)
        # 1. Iterate over each row of the csv file.
        for row_id, row_val in reader:
            # 2. Clean and Redis-key-format each row's string data.
            user_id = str(row_id).replace('[', '').replace(']', '').strip()
            follows_arr = [str(f.strip()) for f in row_val.replace('[', '').replace(']', '').split(',')]
            # 3. Iterate over the set of user_ids this user follows, adding this user to each's followedBy set.
            for follows_id in follows_arr:
                redis_cnx.sadd(followed_by_key.format(follows_id), user_id)


def report_performance(overall_secs, strat_num, posting=True):
    """Formats and prints the function's performance time."""
    # 1. Determine conditional formatting.
    twitter_obj, num_iters = ('post', 1_000_000) if posting else ('timeline', 10)
    report_title = 'strategy {}: {}s'.format(strat_num, twitter_obj)
    # 2. Calculate results metrics.
    secs_per_obj = (overall_secs / num_iters)
    objs_per_sec = secs_per_obj ** (-1)
    # 3. Instantiate format templates.
    float_fmt = '{:<20}{:>20,.8f}'
    int_fmt = '{:<20}{:>20,.0f}'
    objs_per_fmt = int_fmt if posting else float_fmt
    # 4. Print report.
    print('{:═^40}'.format(''))
    print('{:^40}'.format(report_title.upper()))
    print('{:─^40}'.format(''))
    print(float_fmt.format('Overall seconds', overall_secs))
    print(float_fmt.format('Seconds per ' + twitter_obj.lower(), secs_per_obj))
    print(objs_per_fmt.format(twitter_obj.title() + 's per second', objs_per_sec))
    print('{:═^40}'.format(''))


def gen_random_users(redis_cnx):
    """Returns an array of randomly sampled user_ids."""
    rand_indices = np.random.randint(0, redis_cnx.llen('user_tweet_ids'), size=10)
    return [redis_cnx.lindex('user_tweet_ids', str(i)).split(':')[1].strip() for i in rand_indices]


def display_timeline(tweets_list, user_id):
    """Formats and prints a user's timeline for easier viewing."""
    print('{:═^116}'.format(''))
    print('{:^116}'.format('USER_ID: ' + str(user_id)))
    print('{:─^116}'.format(''))
    print('{:┈^116}'.format(''))
    for tweet_dict in tweets_list:
        print('{:<20}{:<20}'.format(tweet_dict['time'], tweet_dict['poster_id']))
        print(tweet_dict['content'])
        print('{:┈^116}'.format(''))
    print('{:═^116}'.format(''))


def connect_to_redis():
    """Establishes a connection to the local Redis database client."""
    try:
        redis_cnx = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True)
        redis_cnx.ping()
        print('... connecting to Redis  ...')
        return redis_cnx
    except redis.exceptions.ConnectionError:
        print('ERROR: Redis connection unsuccessful!')
        exit(1)


def calc_execution_time(func_to_time, redis_cnx, strat_num, is_posting=True):
    """Executes and times the given function call depending on its type."""
    if is_posting:
        start_time = time.time()
        func_to_time(redis_cnx)
        end_time = time.time()
        elapsed_time = end_time - start_time
    else:
        user_ids_arr = gen_random_users(redis_cnx)
        start_time = time.time()
        func_to_time(redis_cnx, user_ids_arr)
        end_time = time.time()
        elapsed_time = end_time - start_time
    report_performance(elapsed_time, strat_num, is_posting)


# STRATEGY 1

def post_tweet_s1(redis_cnx, tweet_arr):
    """Posts the given tweet to the master stream generating a unique tweet_id."""
    tweet_val = 'poster:{}:tweet:{}'
    redis_cnx.lpush('user_tweet_ids', tweet_val.format(str(tweet_arr[1]), str(tweet_arr[0])))
    redis_cnx.hmset(tweet_arr[0], {'poster_id': tweet_arr[1], 'time': tweet_arr[2], 'content': tweet_arr[3]})


def post_data_s1(redis_cnx, filepath='./data/tweets.csv'):
    """Posts all tweets in the file with the given path."""
    with open(filepath, 'r', encoding='utf8') as in_file:
        reader = csv.reader(in_file)
        for tweet in reader:
            post_tweet_s1(redis_cnx, tweet)


def get_timeline_s1(redis_cnx, user_id):
    """Returns the timeline of the given user; accumulates tweets 'on-the-fly'."""
    follows_key = 'user:{}:follows'
    follows_set = {m.strip() for m in redis_cnx.smembers(follows_key.format(str(user_id)))}
    res_arr = list()
    i = 0
    while len(res_arr) < 10:
        i += 1
        post_query = redis_cnx.lindex('user_tweet_ids', i)
        if post_query is None:
            break
        else:
            post_ids = post_query.split(':')
            if post_ids[1] in follows_set:
                res_arr.append(redis_cnx.hgetall(post_ids[3]))
            else:
                continue
    return res_arr


def get_rand_timelines_s1(redis_cnx, users_arr):
    """Returns the timelines for the given array of user ids."""
    for user_id in users_arr:
        display_timeline(get_timeline_s1(redis_cnx, user_id), user_id)


# STRATEGY 2

def post_tweet_s2(redis_cnx, tweet_arr):
    """Copies tweet to user's home timeline automatically."""
    redis_cnx.lpush('user_tweet_ids', str(tweet_arr[1]) + ':' + str(tweet_arr[0]))
    redis_cnx.hmset(tweet_arr[0], {'poster_id': tweet_arr[1], 'time': tweet_arr[2], 'content': tweet_arr[3]})
    followed_by_key = 'user:{}:followedBy'
    followed_by_set = {m.strip() for m in redis_cnx.smembers(followed_by_key.format(str(tweet_arr[1])))}
    for user_id in followed_by_set:
        timeline_key = 'timeline:{}'
        redis_cnx.lpush(timeline_key.format(user_id), tweet_arr[0])


def post_data_s2(redis_cnx, filepath='./data/tweets.csv'):
    """Posts all tweets in the file with the given path."""
    with open(filepath, 'r', encoding="utf8") as in_file:
        reader = csv.reader(in_file)
        for tweet in reader:
            post_tweet_s2(redis_cnx, tweet)


def get_timeline_s2(redis_cnx, user_id):
    """Returns the pre-written timeline of the given user."""
    timeline_key = 'timeline:{}'
    timeline_ids = redis_cnx.lrange(timeline_key.format(user_id), 0, 9)
    return [redis_cnx.hgetall(i) for i in timeline_ids]


def get_rand_timelines_s2(redis_cnx, users_arr):
    """Returns the timelines for the given array of user ids."""
    for user_id in users_arr:
        display_timeline(get_timeline_s2(redis_cnx, user_id), user_id)


# MAIN

def main():
    """Runs our program's performance analysis."""
    print('Running `ds4300_hw2.py` performance analysis ...')
    redis_cnx = connect_to_redis()
    if input('Reload follower relationships? Y/N: \t') == 'Y':
        print('... loading user-follows relationships ...')
        load_follows(redis_cnx)
        print('... loading user-followed_by relationships ...')
        load_followed_by(redis_cnx)
    print('... running Strategy 1: Post ...')
    calc_execution_time(post_data_s1, redis_cnx, 1)
    print('... running Strategy 1: Retrieve ...')
    calc_execution_time(get_rand_timelines_s1, redis_cnx, 1, False)
    print('... running Strategy 2: Post ...')
    calc_execution_time(post_data_s2, redis_cnx, 2)
    print('... running Strategy 2: Retrieve ...')
    calc_execution_time(get_rand_timelines_s2, redis_cnx, 2, False)
    print('... Done.')


if __name__ == "__main__":
    main()
