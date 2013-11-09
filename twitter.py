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
        package = {}
        if 'coordinates' in data and data['coordinates'] is not None:
            package["coordinates"] = data['coordinates']['coordinates']
            package["text"] = data['text']
            myStreamer.ex.append(package)
            if(len(myStreamer.ex) > 50):
                with open("test.txt","w") as f:
                    for elem in myStreamer.ex:
                        f.write(str(elem) + "\n")
                    print myStreamer.ex
                    myStreamer.ex = []
                    print myStreamer.ex
        """
        parsed = {}
        else:
            print data["user"]["location"]
            city = data["user"]["location"].split()[0].strip(',').lower()
            state = data["user"]["location"].split()[1]
            catch_json = urllib2.urlopen('http://api.geonames.org/searchJSON?q=' + city + '&maxRows=' + str(NUMCITIES) + '&username=cmiller0330')
            open_json = ast.literal_eval(catch_json.read())
            i = 0
            while (i < NUMCITIES):
                if (open_json["geonames"][i] and "adminCode1" in open_json["geonames"][i] and open_json["geonames"][i]["adminCode1"] == state):
                    parsed["coordinates"] = [
                        float(open_json["geonames"][i]["lat"]), float(open_json["geonames"][i]["lng"])]
                    break
                else:
                    parsed["coordinates"] = []
                i += 1
        parsed["hashtags"] = data["entities"]["hashtags"]
        parsed["screen_name"] = "@" + data["entities"]["user_mentions"][0]["screen_name"]
        parsed["text"] = data["text"]
        """
        #if 'place' in data and data['place'] is not None:
        #    print data['place']
        #if "user" in data and data["user"] is not None:
        #    if "location" in data["user"] and data["user"]["location"] is not None:
        #        print data["user"]["location"]

    def on_error(self, status_code, data):
        print status_code
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect


def twitter_auth1(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def twitter_auth2(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET):
    """
    Returns a Twython object that is fully logged in and ready to go.
    """
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, access_token=ACCESS_TOKEN)


def json_parse(data):
    NUMCITIES = 10
    parsed = {}
    data = json.dump(data)
    print "load works."

    if ("coordinates" in data and "coordinates" in data["coordinates"]):
        parsed["coordinates"] = data["coordinates"]["coordinates"]
    else:
        city = data["user"]["location"].split()[0].strip(',').lower()
        state = data["user"]["location"].split()[1]
        catch_json = urllib2.urlopen(
            'http://api.geonames.org/searchJSON?q=' + city + '&maxRows=' + str(NUMCITIES) + '&username=cmiller0330')
        open_json = ast.literal_eval(catch_json.read())
        i = 0
        while (i < NUMCITIES):
            if (open_json["geonames"][i] and "adminCode1" in open_json["geonames"][i] and open_json["geonames"][i]["adminCode1"] == state):
                parsed["coordinates"] = [
                    float(open_json["geonames"][i]["lat"]), float(open_json["geonames"][i]["lng"])]
                break
            else:
                parsed["coordinates"] = []
            i += 1
    parsed["hashtags"] = data["entities"]["hashtags"]
    parsed["screen_name"] = "@" + \
        data["entities"]["user_mentions"][0]["screen_name"]
    parsed["text"] = data["text"]
    print parsed

if __name__ == "__main__":
    stream = myStreamer(
        CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=GENERIC,location=USA)
