import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

from database.db_manager import DBManager
from database.CRUD.read import *
from database.model import Trend, Tweet, User
import pandas as pd
import time
import json

# Get the eldest user registered in the Users collection of the Twitter database.
def get_eldest_user():
    # get all users
    users = User.nodes.all()
    # get all the users for which joined_date is not null
    users = [user for user in users if user.joined_date is not None]
    # sort users by joined_date
    users.sort(key=lambda x: x.joined_date)
    # return the eldest user
    return {
        "username": users[0].username,
        "followers": users[0].followers,
        "following": users[0].following,
        "verified": users[0].verified,
        "joined_date": users[0].joined_date
    } if len(users) > 0 else None
        
# Get the k most shared tweets in the Tweets collection of the Twitter database.
def get_k_most_shared_tweets(k):
    # get all tweets
    tweets = Tweet.nodes.all()
    # sort tweets by shares
    tweets.sort(key=lambda x: x.shares, reverse=True)
    # return the k most shared tweets
    return [ { "url": tweet.url, "username": tweet.username, "text": tweet.text, "sentiment": tweet.sentiment, "retweets": tweet.retweets, "likes": tweet.likes, "shares": tweet.shares } for tweet in tweets ][:k]
    
# Get the trends for which more than minTweets tweets have been written
def get_k_most_popular_trends(minTweets):
    # get all trends
    trends = Trend.nodes.all()
    # filter trends by number of tweets
    trends = [trend for trend in trends if len(trend.tweets) > minTweets]
    # sort trends by number of tweets
    trends.sort(key=lambda x: len(x.tweets), reverse=True)
    # return the k most popular trends
    return [ { "url": trend.url, "name": trend.name, "location": trend.location, "date": trend.date } for trend in trends ][:minTweets]

# Get the most popular users in the Users collection of the Twitter database given a minimum threshold of followers.
def get_k_most_popular_users(minFollowers):
    # get all users
    users = User.nodes.all()
    # filter users by number of followers
    users = [user for user in users if user.followers > minFollowers]
    # sort users by number of followers
    users.sort(key=lambda x: x.followers, reverse=True)
    # return the k most popular users
    return [ { "username": user.username, "followers": user.followers, "following": user.following, "verified": user.verified } for user in users ][:minFollowers]

PERFORMANCES = True
NUM_TESTS = 10

if __name__ == '__main__':
    
    # take port, name of the db, username and password from the command line
    if len(sys.argv) != 5:
        print("Usage: python create.py <port> <db_name> <username> <password>")
        sys.exit(1)
    
    db_manager = DBManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
    operations = [
        {
            "name": "GET ELDEST USER",
            "operation": get_eldest_user,
            "parameters": []
        },
        {
            "name": "GET MOST SHARED TWEETS",
            "operation": get_k_most_shared_tweets,
            "parameters": [10]
        },
        {
            "name": "GET POPULAR TRENDS",
            "operation": get_k_most_popular_trends,
            "parameters": [5]
        },
        {
            "name": "GET POPULAR USERS",
            "operation": get_k_most_popular_users,
            "parameters": [10000]
        }
    ]

    if not PERFORMANCES:

        for operation in operations:
            print(operation["name"])
            if len(operation["parameters"]) == 0:
                print(json.dumps(operation["operation"](), indent=4))
            else:
                print(json.dumps(operation["operation"](*operation["parameters"]), indent=4))
    
    else:
        
        perf = pd.DataFrame(columns=['operation', 'executionTime'])
        
        for n in range(NUM_TESTS):
            
            print("Test " + str(n + 1))
            
            for operation in operations:
                    
                print(operation["name"])
                
                start = time.time()
                
                if len(operation["parameters"]) == 0:
                    operation["operation"]()
                else:
                    operation["operation"](*operation["parameters"])
                    
                end = time.time()
                
                perf = perf._append({
                    'operation': operation["name"],
                    'executionTime': end - start
                }, ignore_index=True)
            
        # compute the mean of the execution times for each operation
        operations = perf['operation'].unique()
        mean_df = pd.DataFrame(columns=['operation', 'executionTime'])
        for operation in operations:
            mean = perf[perf['operation'] == operation]['executionTime'].mean()
            # replace the rows with the mean
            mean_df = mean_df._append({
                'operation': operation,
                'executionTime': mean
            }, ignore_index=True)
        mean_df.to_csv('performances/other_queries_performances_GDB.csv', index=False)