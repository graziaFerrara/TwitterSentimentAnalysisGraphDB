import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

from database.db_manager import DBManager
from database.model import Trend, Tweet, User

# mongo_id

def get_tweet_by_mongo_id(id_mongo_tweet):
    return Tweet.nodes.get(id_mongo=id_mongo_tweet)

def get_trend_by_mongo_id(id_mongo_trend):
    return Trend.nodes.get(id_mongo=id_mongo_trend)

def get_user_by_mongo_id(id_mongo_user):
    return User.nodes.get(id_mongo=id_mongo_user)

# url

def get_tweet_by_url(url_tweet):
    return Tweet.nodes.get_or_none(url=url_tweet)

def get_trend_by_url(url_user):
    return Trend.nodes.get_or_none(url=url_user)

# username 

def get_user_by_username(username):
    return User.nodes.get_or_none(username=username)

# name, location, date

def get_trend_by_name_location_date(name, location, date):
    return Trend.nodes.get_or_none(name=name, location=location, date=date)

# retrieve information from links

def get_trends_by_tweet(tweet):
    if tweet is None:
        return None
    return tweet.trends.all()

def get_tweets_by_trend(trend):
    if trend is None:
        return None
    return trend.tweets.all()

def get_tweets_by_user(user):
    if user is None:
        return None
    return user.tweets.all()

def get_user_by_tweet(tweet):
    if tweet is None:
        return None
    return tweet.user.all()

def get_comments_by_tweet(tweet):
    if tweet is None:
        return None
    return tweet.comments_from.all()

if __name__ == '__main__':

    # take port, name of the db, username and password from the command line
    if len(sys.argv) != 5:
        print("Usage: python create.py <port> <db_name> <username> <password>")
        sys.exit(1)
    
    db_manager = DBManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    # 1. GET TRENDS BY TWEET GIVEN TWEET MONGO ID
    print("GET TRENDS BY TWEET GIVEN TWEET MONGO ID")
    print(get_trends_by_tweet(get_tweet_by_mongo_id("654270427e0338fef46ed41b")))

    # 2. GET TRENDS BY TWEET GIVEN TWEET URL
    print("GET TRENDS BY TWEET GIVEN TWEET URL")
    print(get_trends_by_tweet(get_tweet_by_url("https://twitter.com/username/status/1719730559793180907")))

    # 3. GET TWEEETS BY TREND GIVEN TREND MONGO ID
    print("GET TWEEETS BY TREND GIVEN TREND MONGO ID")
    print(get_tweets_by_trend(get_trend_by_mongo_id("65426edb7e0338fef46ed3eb")))

    # 4. GET TWEEETS BY TREND GIVEN TREND URL
    print("GET TWEEETS BY TREND GIVEN TREND URL")
    print(get_tweets_by_trend(get_trend_by_url("https://twitter.com/search?q=%23Halloween&src=trend_click&vertical=trends")))

    # 5. GET TWEEETS BY TREND GIVEN TREND NAME, LOCATION AND DATE
    print("GET TWEEETS BY TREND GIVEN TREND NAME, LOCATION AND DATE")
    print(get_tweets_by_trend(get_trend_by_name_location_date("#Halloween", "Italy", "2023-11-01T16:29:31.292726")))

    # 6. GET TWEETS BY USER GIVEN USER MONGO ID
    print("GET TWEETS BY USER GIVEN USER MONGO ID")
    print(get_tweets_by_user(get_user_by_mongo_id("654270367e0338fef46ed40e")))

    # 7. GET TWEETS BY USER GIVEN USER USERNAME
    print("GET TWEETS BY USER GIVEN USER USERNAME")
    print(get_tweets_by_user(get_user_by_username("@bobuxhunter")))

    # 8. GET USER BY TWEET GIVEN TWEET MONGO ID
    print("GET USER BY TWEET GIVEN TWEET MONGO ID")
    print(get_user_by_tweet(get_tweet_by_mongo_id("654270427e0338fef46ed41b")))

    # 9. GET USER BY TWEET GIVEN TWEET URL
    print("GET USER BY TWEET GIVEN TWEET URL")
    print(get_user_by_tweet(get_tweet_by_url("https://twitter.com/username/status/1719730559793180907")))

    # 10. GET COMMENTS BY TWEET GIVEN TWEET MONGO ID
    print("GET COMMENTS BY TWEET GIVEN TWEET MONGO ID")
    print(get_comments_by_tweet(get_tweet_by_mongo_id("6542702c7e0338fef46ed406")))

    # 11. GET COMMENTS BY TWEET GIVEN TWEET URL
    print("GET COMMENTS BY TWEET GIVEN TWEET URL")
    print(get_comments_by_tweet(get_tweet_by_url("https://twitter.com/username/status/1713864866136821794/analytics")))
