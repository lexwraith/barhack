import pandas as pd
import json

from datetime import datetime
from collections import namedtuple
from twython import Twython

USERNAME = "lexwraith"
PASSWORD = "PassWord"

TWITTER_REQUEST_LIMIT = 100  # How many user JSONs I can pull per request
TWITTER_RATE_LIMIT = 180  # How many requests per 15 minutes

AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "crd6qE1BNWFWqZhVXfBtug"
CONSUMER_SECRET = "ND8Wd59Dw8Cju7uezeTmJuSowjbGsDiXwajRvzVfQ"
OAUTH_TOKEN = "635136003-bmxyoG4XmsqslD2gwpE4UODqde9TpLc6PYkD0nFt"


def extract(dataframe, names_label="screen_name", column="followers_count", sort_column=1):
    """
    Pulls out a sorted list with names_label and sorted by the column argument.
    """
    package = []
    for z in range(len(dataframe)):
        package.append((dataframe[names_label][z], dataframe[column][z]))
    return sorted(package, key=lambda x: x[sort_column])


def twitter_auth(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
    """
    Returns a Twython object that is fully logged in and ready to go.
    """
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, access_token=ACCESS_TOKEN)


def getStuff(t):
    """
    Pulls out useful information from a Twitter JSON.
    Returns it in namedTuple format...?
    """
    daysAlive = (
        datetime.strptime(str(t["created_at"]), "%a %b %d %H:%M:%S") - datetime.today()).days
    favoritesCount = t["favourites_count"]
    followersCount = t["followers_count"]
    followingCount = t["friends_count"]
    listsCount = t["listed_count"]
    location = t["location"]
    #profile = None
    tweetCount = t["statuses_count"]
    #URL = t["url"]
    boolVerified = t["verified"]
    boolContrib = t["contributors_enabled"]
    favsPerDay = favoritesCount / float(daysAlive)
    folsPerDay = followersCount / float(daysAlive)
    listsPerDay = listsCount / float(daysAlive)
    print daysAlive,favoritesCount,followersCount,followingCount,listsCount,location,tweetCount,boolVerified,boolContrib,favsPerDay,folsPerDay,listsPerDay


def twitter_lookup(userbatch):
    """
    Returns a large JSON object.

    Note that Twitter followers who have deactivated their accounts will
    not appear on the end result.
    """
    assert type(userbatch) == list ,"Argument is supposed to be a list!"
    twitter = twitter_auth()
    batches = []
    while(len(userbatch) > TWITTER_REQUEST_LIMIT):
        batches.append(convertListToCSV(userbatch[:TWITTER_REQUEST_LIMIT]))
        userbatch = userbatch[TWITTER_REQUEST_LIMIT:]
    batches.append(convertListToCSV(userbatch[:]))
    for elem in range(len(batches)):
        batches[elem] = pd.read_json(
            json.dumps(twitter.lookup_user(screen_name=batches[elem])))
    return pd.concat(batches, ignore_index=True)

if __name__ == "__main__":
    t = twitter_auth()
    t.search(q='food',result_type='popular')