import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

import json
from neomodel import db
from database.model import Trend, Tweet, User
from neo4j import GraphDatabase

if __name__ == "__main__":

    # take port, name of the db, username and password from the command line
    if len(sys.argv) != 5:
        print("Usage: python create.py <port> <db_name> <username> <password>")
        sys.exit(1)

    port = sys.argv[1]
    db_name = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]

    uri = f"bolt://localhost:{port}/{db_name}"

    # Create a Neo4j driver instance
    driver = GraphDatabase.driver(uri, auth=(username, password))
    db.set_connection(uri, driver)

    # read json files
    def read_json(file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data

    # list the files in the database/data/ directory
    files = []
    with os.scandir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/') as entries:
        for entry in entries:
            if entry.is_file():
                files.append(entry.path)

    trends_files = []
    tweets_files = []
    users_files = []

    for file in files:
        filename = file.split("/")[-1].lower()
        if "tweets" in filename:
            tweets_files.append(file)
        elif "users" in filename:
            users_files.append(file)
        elif "trends" in filename:
            trends_files.append(file)

    trends = [trend for file in trends_files for trend in read_json(file)]
    tweets = [tweet for file in tweets_files for tweet in read_json(file)]
    users = [user for file in users_files for user in read_json(file)]

    # delete all nodes and relationships
    db.cypher_query("MATCH (n) DETACH DELETE n")

    # CREATE NODES

    # create trends
    for trend in trends:
        t = Trend(id_mongo=trend["_id"], url=trend["url"], name=trend["name"], location=trend["location"], date=trend["date"]).save()

    # create users
    for user in users:
        u = User(id_mongo=user["_id"], username=user["username"], followers=user["followers"], following=user["following"], verified=user["verified"]).save()

    # create tweets
    for tweet in tweets:
        t = Tweet(id_mongo=tweet["_id"], url=tweet["url"], username=tweet["username"], text=tweet["text"], sentiment=tweet["sentiment"], retweets=tweet["retweets"], likes=tweet["likes"], shares=tweet["shares"]).save()

    # create tweets from tweets comments
    for tweet in tweets:
        if "comments" in tweet:
            for comment in tweet["comments"]:
                t = Tweet(id_mongo=comment["_id"], url=comment["url"], username=comment["username"], text=comment["text"], sentiment=comment["sentiment"], retweets=comment["retweets"], likes=comment["likes"], shares=comment["shares"]).save()

    # CREATE RELATIONSHIPS

    # create relationships between trends and tweets
    for trend_data in trends:
        for tweet_id in trend_data["tweets"]:
            tweet = Tweet.nodes.get(id_mongo=tweet_id)
            trend = Trend.nodes.get(id_mongo=trend_data["_id"])
            if tweet and trend:
                tweet.trend.connect(trend)
            else:
                print(f"Tweet or Trend not found for ids: {tweet_id}, {trend_data['_id']}")

    # create relationships between tweets and users
    for user_data in users:
        for tweet_id in user_data["tweets"]:
            try:
                tweet = Tweet.nodes.get(id_mongo=tweet_id)
                user = User.nodes.get(id_mongo=user_data["_id"])
                tweet.user.connect(user)
            except:
                print(f"Tweet or User not found for ids: {tweet_id}, {user_data['_id']}")

    # create relationships between tweets and their comments which are tweets
    for tweet_data in tweets:
        if "comments" in tweet_data:
            for comment_id in tweet_data["comments"]:
                try:
                    comment = Tweet.nodes.get(id_mongo=comment_id["_id"])
                    tweet = Tweet.nodes.get(id_mongo=tweet_data["_id"])
                    comment.comments.connect(tweet)
                except:
                    print(f"Tweet or Comment not found for ids: {comment_id['_id']}, {tweet_data['_id']}")

            