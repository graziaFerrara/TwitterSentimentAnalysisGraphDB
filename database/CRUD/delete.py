import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

from database.db_manager import DBManager
from database.model import Trend, Tweet, User
from database.CRUD.read import *

def delete(entity):
    """
    The delete function deletes an entity.
    
    :param entity: The "entity" parameter is an object that represents a specific entity in your code.
    The "delete" function is used to delete or remove that entity from your code or from any associated
    data storage
    """
    entity.delete()

if __name__ == '__main__':
    
    # take port, name of the db, username and password from the command line
    if len(sys.argv) != 5:
        print("Usage: python delete.py <port> <db_name> <username> <password>")
        sys.exit(1)

    try:
        db_manager = DBManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    except:
        print("Error while connecting to the database")
        sys.exit(1)

    tweet = get_tweet_by_url("https://twitter.com/username/status/1714204269056823745/analytics")
    trend = get_trend_by_url("https://twitter.com/search?q=%23bonustrasporti&src=trend_click&vertical=trends")
    user = get_user_by_username("@Siftedeu")

    # delete relationship between user and tweet
    db_manager.delete_relationship_by_nodes(user.element_id.split(":")[-1], tweet.element_id.split(":")[-1], "POSTED_BY")
    
    # delete relationship between tweet and trend
    db_manager.delete_relationship_by_nodes(tweet.element_id.split(":")[-1], trend.element_id.split(":")[-1], "RELATED_TO")

    # delete realtionship between tweet and comment
    for comment in get_comments_by_tweet(tweet):
        db_manager.delete_relationship_by_nodes(comment.element_id.split(":")[-1], tweet.element_id.split(":")[-1], "COMMENTED_ON")

    # # delete tweet
    delete(tweet)

    # # delete trend
    delete(trend)

    # # delete user
    delete(user)

    # delete all relationships of a specific type

    # delete all relationships of type "RELATED_TO"

    # delete all relationships of type "POSTED_BY"

    # delete all relationships of type "COMMENTED_ON"

    # delete all tweets

    # delete all trends

    # delete all users

    