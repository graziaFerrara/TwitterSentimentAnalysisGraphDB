import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

from database.db_manager import DBManager
from database.model import Trend, Tweet, User
from database.CRUD.read import *

def update(entity, properties: dict):
    """
    The `update` function updates the properties of an entity object with the values provided in the
    `properties` dictionary and saves the changes.
    
    :param entity: The `entity` parameter is an object that you want to update with new property values
    :param properties: A dictionary containing the properties to be updated. The keys of the dictionary
    represent the property names, and the values represent the new values for those properties
    :type properties: dict
    :return: nothing.
    """
    if entity is None:
        return
    for property_name, property_value in properties.items():
        if not hasattr(entity, property_name):
            continue
        setattr(entity, property_name, property_value)
    entity.save()

if __name__ == '__main__':

    # take port, name of the db, username and password from the command line
    if len(sys.argv) != 5:
        print("Usage: python create.py <port> <db_name> <username> <password>")
        sys.exit(1)

    db_manager = DBManager(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    # update tweet
    tweet = get_tweet_by_url("https://twitter.com/username/status/1719675501650792714")
    update(tweet, {"retweets": 10, "likes": 20, "shares": 30})

    # update trend
    trend = get_trend_by_url("https://twitter.com/search?q=%23Meloni&src=trend_click&vertical=trends")
    update(trend, {"name": "Meloni", "location": "Worldwide", "date": "2021-10-31"})

    # update user
    user = get_user_by_username("@Iconicspeakerss")
    update(user, {"followers": 100, "following": 200, "verified": True})
