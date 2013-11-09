import pandas as pd
import json
import django.http

from pprint import pprint
from datetime import datetime
from collections import namedtuple
from twython import Twython
from twython import TwythonStreamer

USERNAME = "lexwraith"
PASSWORD = "PassWord"

TWITTER_REQUEST_LIMIT = 100  # How many user JSONs I can pull per request
TWITTER_RATE_LIMIT = 180  # How many requests per 15 minutes

AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "1U4kULn0xaVfoX8WjtPPLg"  # barhack
CONSUMER_SECRET = "ZHGirEpnFi8vLWQH9WhFVvqmtNp06XpkyTkb89NM"  # barhack
OAUTH_TOKEN = "635136003-7jE8u2yLYPONdR11bMEDyHSGc1ZVFVzG7NeoK0SN"
OAUTH_TOKEN_SECRET = "5mmff9ewLChIeP3jV5rb5DR6f4ylRVF0To2VSZVRC5DFM"


class myStreamer(TwythonStreamer):

    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


def twitter_auth1(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def twitter_auth2(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
    """
    Returns a Twython object that is fully logged in and ready to go.
    """
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, access_token=ACCESS_TOKEN)


def twitter_lookup(userbatch):
    """
    Returns a large JSON object.

    Note that Twitter followers who have deactivated their accounts will
    not appear on the end result.
    """
    assert isinstance(userbatch, list), "Argument is supposed to be a list!"
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
    stream = myStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    