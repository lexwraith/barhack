import pandas as pd
import json
import django.http
import json
import urllib2
import ast

from pprint import pprint
from datetime import datetime
from collections import namedtuple
from twython import Twython
from twython import TwythonStreamer

USA = "-124.624960,48.368122,-80.477557"
SF = "-122.75,36.8,-121.75,37.8"
GENERIC = "the,be,to,of,and,a,in,that,have,I,it,for,not,on,with,he,as,you,do,at,this,but,his,by,from"

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
    ex = []

    def on_success(self, data):
        if 'coordinates' in data and data['coordinates'] is not None:
            myStreamer.ex.append(
                [data['coordinates']['coordinates'][0], data['coordinates']['coordinates'][1], data['text'].encode('ascii')])
            if len(myStreamer.ex) > 5:
                self.dumpEx()
                myStreamer.ex = []

    def on_error(self, status_code, data):
        print status_code
        # self.disconnect

    def dumpEx(self):
        f = open("testdata.txt", "w")
        for elem in myStreamer.ex:
            print elem
            f.write(str(elem[0]) + "," + str(elem[1]) + "," + str(elem[2]) + "\n")
        f.close()

def twitter_auth1(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def twitter_auth2(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
    """
    Returns a Twython object that is fully logged in and ready to go.
    """
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, access_token=ACCESS_TOKEN)

if __name__ == "__main__":
    stream = myStreamer(
        CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=GENERIC, location=USA)
