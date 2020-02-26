CODE AUTHOR: Brian Fogarty
PERFORMANCE ANALYSIS AUTHORS: Kristie Wong, Vidhi Gondalia

Changed assumptions: From HW1, we changed the number of followers each of the users had from 3 to a range 10-20.
This ensured that we were able to retrieve at least 10 tweets per user timeline. This did not let us compare SQL and 
Redis performance direct but despite the change in followers we found that Redis was relatively faster than MySQL for 
timeline retrieval.

3.1. How do the two strategies compare? The write performance of posting a tweet is better for strategy 1 because it 
simply involves creating a key-value pair for the poster and tweet. No queueing to followers' timelines is involved. 
In contrast, strategy 2 is slower because the key-value pair not only has to be made, but a copy must be queued to every 
follower's timeline. This makes the read time of generating timelines faster for strategy 2. Instead of generating one-off 
timelines at the time of the request, we can simply pull the 10 most recent tweets queued to the timeline list. 
For strategy 1, we had to pull the user's follower list and compare the followers' user_ids against all recent tweet 
poster ids until we found 10.

3.2. How does Redis comapre with MySQL? Compared to MySQL where 2525 tweets were posted per second, we could post 2123 
tweets per second in Redis. Which implied that posting was slower in Redis than in MYSQL. However, MySQL was only able
to retrieve 0.2691 timelines (given that there were only 3 tweets per timeline) and Redis was able to retrieve ____. 


Strategy 1: 
To post a tweet, a key-value is sent to a master stream of tweets. Each tweet has a uniquely generated tweet_id.
To generate a timeline, we must look at the master stream of tweets in chronological order. We compare the poster's 
ids against the user's following list. When a poster is followed by the user, we add the tweet to the timeline. We stop 
when the timeline hits 10 tweets.
This results in faster writes and slower reads.

Post Tweet Functions:
1. The function post_tweet_s1(tweet_arr) takes in a tweet array (with tweet id, poster's user_id, content, and post time).
We push the tweet to a master stream called user_tweet_ids. We create a set with the key as tweet_id. It is mapped to the 
posted tweet's user id, post time, and tweet content.
No queueing is done.

2. The function post_data_s1(filepath='./data/tweets.csv') passes in every line in the given csv. Each line represents a tweet
that needs to be posted.
The lines of tweets are posted using post_tweet_s1(tweet_arr).

We timed the posting of our 1 million tweet csv and reported thea performance based on overall seconds, seconds per timeline,
and timelines per second.

Get Timeline Functions
1. The function get_timeline_s1(user_id) takes in a given user's id and generates the timeline of the 10 most recent tweets 
posted by people the user is following at the time of the request.
We create a list representing the timeline called res_arr. We look through all posts in chronological order. When a post's
poster is followed by the given user, we push a reference to the tweet via tweet_id to the timeline.
The function stops when the timeline hits 10 posts or there are no more posts to check.

2. The function get_rand_timelines_s1(users_arr) was used to generate the timelines of the given array of user ids.

We used this to test our performance by passing in 10 random users to generate timelines for and timing the performance.


Strategy 2: 
As tweets are posted, they are immediately pushed to the poster's follower's queued timelines. This results in slower writes and faster reads.

Post Tweet Functions:
1. The function post_tweet_s2(tweet_arr) takes in a tweet (with its poster's user_id, content, and post time).
It adds the tweet onto the head of a list called user_tweet_ids. The values added are the poster's user id, the tweets post time, and the tweet content.
Every user has a queued timeline named timeline:{the user's id}.
After posting a tweet, we add that tweet onto the head of every follower of the user's queued timeline.

2. The function post_data_s2(filepath='./data/tweets.csv') passes in every line in the given csv. Each line represents a tweet that needs to be posted.
The lines of tweets are posted using post_tweet_s2(tweet_arr).

We timed the posting of our 1 million tweet csv and reported the performance based on overall seconds, seconds per timeline, and timelines per second.

Get Timeline Functions:
1. The function get_timeline_s2(user_id) takes in a given user's id and generates the timeline by displaying the 10 most recent (the first 10) tweets from that user's queued timeline.
The queued timeline can be pulled using the key timeline:{the user's id}.

2. The function get_rand_timelines_s2(users_arr) was used to generate the timelines of the given array of user ids.

We used this to test our performance by passing in 10 random users to generate timelines for and timing the performance.
