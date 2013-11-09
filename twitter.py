import pandas as pd
import json
import django.http
import json
import urllib2
import ast
import random

from pprint import pprint
from datetime import datetime
from collections import namedtuple
from twython import Twython
from twython import TwythonStreamer

USA = "24.396,-124.624,49.384,-66.88"
USA = "-124,24,-66,50"
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
        parsed = {}
        NUMCITIES = 10
        city = ""
        state = 0

        if 'coordinates' in data and data['coordinates'] is not None:
            parsed['coordinates'] = data['coordinates']['coordinates']
        else:
            if 'user' in data and data['user'] is not None:
                location = data['user']['location']
                if (',' in location):
                    location = location.partition(',')
                    if (len(location) == 3):
                        city = location[0].strip().lower().replace(' ', '_')
                        if (len(location[2].strip()) == 2):
                            state = location[2].strip().upper()
                        else:
                            state = location[2].strip().upper()[0:2]
                else:
                    city = location.lower().replace(' ', '_')
            catch_json = urllib2.urlopen(
                'http://api.geonames.org/searchJSON?q=' + city + '&maxRows=' + str(NUMCITIES) + '&username=cmiller0330' + '&country=US')
            open_json = ast.literal_eval(catch_json.read())
            if 'geonames' in open_json and open_json['geonames'] is not None:
                for i in range(min(NUMCITIES,len(open_json['geonames']))):
                    if (isinstance(state, int)):
                        first = 0
                        first = random.randint(0,min(NUMCITIES,len(open_json['geonames'])-1))
                        parsed['coordinates'] = float(open_json['geonames'][first]["lat"]), float(
                            open_json['geonames'][first]['lng'])
                        break
                    elif open_json['geonames'][i] and 'adminCode1' in open_json["geonames"][i] and open_json['geonames'][i]['adminCode1'] == state:
                        parsed["coordinates"] = [
                            float(open_json["geonames"][i]["lat"]), float(open_json["geonames"][i]["lng"])]
                        break
        #parsed['screen_name'] = '@' + data['entities']['user_mentions'][0]['screen_name']
        if 'text' in data:
            parsed['text'] = data['text'].encode('ascii', 'ignore')
            if 'coordinates' in parsed:
                print [parsed['text'],parsed['coordinates']]
        else:
            pass

    def on_error(self, status_code, data):
        print status_code
        # self.disconnect

    def dumpEx(self):
        f = open("testdata.txt", "w")
        for elem in myStreamer.ex:
            print elem
            f.write(str(elem[0]) + "," + str(
                elem[1]) + "," + str(elem[2]) + "\n")
        f.close()


def json_parse(json_file):
    parsed = {}
    json_data = open(json_file)
    data = json.load(json_data)
    NUMCITIES = 10

    if ("coordinates" in data and "coordinates" in data["coordinates"]):
            parsed["coordinates"] = data["coordinates"]["coordinates"]
    else:
        state = 0
        location = data["user"]["location"]
        if (',' in location):
            location = location.partition(',')
            if (len(location) == 3):
                city = location[0].strip().lower().replace(' ', '_')
                if (len(location[2].strip()) == 2):
                    state = location[2].strip().upper()
                else:
                    state = location[2].strip().upper()[0:2]
        else:
            city = location.lower().replace(' ', '_')

        print(city, state)
        catch_json = urllib2.urlopen(
            'http://api.geonames.org/searchJSON?q=' + city + '&maxRows=' + str(NUMCITIES) + '&username=cmiller0330')
        open_json = ast.literal_eval(catch_json.read())

        i = 0
        while (i < NUMCITIES):
            if (len(open_json["geonames"]) > 0):
                if (isinstance(state, int)):
                    parsed["coordinates"] = [
                        float(open_json["geonames"][0]["lat"]), float(open_json["geonames"][0]["lng"])]
                    break
                elif (open_json["geonames"][i] and "adminCode1" in open_json["geonames"][i] and open_json["geonames"][i]["adminCode1"] == state):
                    parsed["coordinates"] = [
                        float(open_json["geonames"][i]["lat"]), float(open_json["geonames"][i]["lng"])]
                    break
                else:
                    parsed["coordinates"] = []
            else:
                parsed["coordinates"] = []
                break
            i += 1

    parsed["hashtags"] = data["entities"]["hashtags"]
    parsed["screen_name"] = "@" + \
        data["entities"]["user_mentions"][0]["screen_name"]
    parsed["text"] = data["text"]

    with open('parsed_tweet.json', 'wb') as fp:
        json.dump(parsed, fp)
    json_data.close()


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
