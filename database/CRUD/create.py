import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

import json
from database.model import Trend, Tweet, User
from database.db_manager import DBManager

# read json files
def read_json(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":

    # take port, name of the db, username and password from the command line
    if len(sys.argv) != 5:
        print("Usage: python create.py <port> <db_name> <username> <password>")
        sys.exit(1)

    try:
        db_manager = DBManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    except:
        print("Error while connecting to the database")
        sys.exit(1)

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
    db_manager.delete_all()

    # create indexes
    db_manager.create_compound_index("name_location_date", "Trend", ["name", "location", "date"])
    db_manager.create_index("mongo_id_trend", "Trend", "mongo_id")
    db_manager.create_index("trend_url", "Trend", "url")
    db_manager.create_index("tweet_url", "Tweet", "url")
    db_manager.create_index("mongo_id_tweet", "Tweet", "mongo_id")
    db_manager.create_index("username", "User", "username")
    db_manager.create_index("mongo_id_user", "User", "mongo_id")

    # CREATE NODES

    # create trends
    for trend in trends:
        t = Trend(id_mongo=trend["_id"], url=trend["url"], name=trend["name"], location=trend["location"], date=trend["date"])
        db_manager.create_node(t)

    # create users
    for user in users:
        u = User(id_mongo=user["_id"], username=user["username"], followers=user["followers"], following=user["following"], verified=user["verified"], joined_date=user["joined_date"])
        db_manager.create_node(u)

    # create tweets
    for tweet in tweets:
        t = Tweet(id_mongo=tweet["_id"], url=tweet["url"], username=tweet["username"], text=tweet["text"], sentiment=tweet["sentiment"], retweets=tweet["retweets"], likes=tweet["likes"], shares=tweet["shares"])
        db_manager.create_node(t)

    # create tweets from tweets comments
    for tweet in tweets:
        if "comments" in tweet:
            for comment in tweet["comments"]:
                t = Tweet(id_mongo=comment["_id"], url=comment["url"], username=comment["username"], text=comment["text"], sentiment=comment["sentiment"], retweets=comment["retweets"], likes=comment["likes"], shares=comment["shares"])
                db_manager.create_node(t)

    # CREATE RELATIONSHIPS

    # create relationships between trends and tweets
    for trend_data in trends:
        for tweet_id in trend_data["tweets"]:
            tweet = Tweet.nodes.get(id_mongo=tweet_id)
            trend = Trend.nodes.get(id_mongo=trend_data["_id"])
            if tweet and trend:
                tweet.trends.connect(trend)
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
                    comment.comments_to.connect(tweet)
                except:
                    print(f"Tweet or Comment not found for ids: {comment_id['_id']}, {tweet_data['_id']}")

            