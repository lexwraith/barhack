import json
import urllib2
import urllib
import ast
import random
import unirest

from pprint import pprint
from twython import Twython
from twython import TwythonStreamer

USA = "24.396,-124.624,49.384,-66.88"
USA = "-124,24,-66,50"
SF = "-122.75,36.82,-121,75,37.8"
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

stateCodes = {
"ALABAMA":"AL",
"ALASKA":"AK",
"AMERICAN SAMOA":"AS",
"ARIZONA":"AZ",
"ARKANSAS":"AR",
"CALIFORNIA":"CA",
"COLORADO":"CO",
"CONNECTICUT":"CT",
"DELAWARE":"DE",
"DISTRICT OF COLUMBIA":"DC",
"FEDERATED STATES OF MICRONESIA":"FM",
"FLORIDA":"FL",
"GEORGIA":"GA",
"GUAM":"GU",
"HAWAII":"HI",
"IDAHO":"ID",
"ILLINOIS":"IL",
"INDIANA":"IN",
"IOWA":"IA",
"KANSAS":"KS",
"KENTUCKY":"KY",
"LOUISIANA":"LA",
"MAINE":"ME",
"MARSHALL ISLANDS":"MH",
"MARYLAND":"MD",
"MASSACHUSETTS":"MA",
"MICHIGAN":"MI",
"MINNESOTA":"MN",
"MISSISSIPPI":"MS",
"MISSOURI":"MO",
"MONTANA":"MT",
"NEBRASKA":"NE",
"NEVADA":"NV",
"NEW HAMPSHIRE":"NH",
"NEW JERSEY":"NJ",
"NEW MEXICO":"NM",
"NEW YORK":"NY",
"NORTH CAROLINA":"NC",
"NORTH DAKOTA":"ND",
"NORTHERN MARIANA ISLANDS":"MP",
"OHIO":"OH",
"OKLAHOMA":"OK",
"OREGON":"OR",
"PALAU":"PW",
"PENNSYLVANIA":"PA",
"PUERTO RICO":"PR",
"RHODE ISLAND":"RI",
"SOUTH CAROLINA":"SC",
"SOUTH DAKOTA":"SD",
"TENNESSEE":"TN",
"TEXAS":"TX",
"UTAH":"UT",
"VERMONT":"VT",
"VIRGIN ISLANDS":"VI",
"VIRGINIA":"VA",
"WASHINGTON":"WA",
"WEST VIRGINIA":"WV",
"WISCONSIN":"WI",
"WYOMING":"WY"
}

def assignPolarity(text):
    response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/", headers={
                            "X-Mashape-Authorization": "q9WreMnPjMW5iL3yNpbnM4jwRmVr6Sbu"}, params={"text": text, "language": "english"})
    sentiment = response.body
    maxval = 0
    maxpol = ''
    for pol in sentiment["probability"]:
        value = sentiment["probability"][pol]
        if (value >= maxval):
            maxval = value
            maxpol = pol
    return [maxpol, maxval]


class myStreamer(TwythonStreamer):
    ex = []
    dumpstate = 1

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
                        elif location[2].strip().upper() in stateCodes:
                            state = location[2].strip().upper()[0:2]
                else:
                    city = location.lower().replace(' ', '_')
            catch_json = urllib2.urlopen(
                'http://api.geonames.org/searchJSON?q=' + city + '&maxRows=' + str(NUMCITIES) + '&username=cmiller0330' + '&country=US')
            open_json = ast.literal_eval(catch_json.read())
            if 'geonames' in open_json and open_json['geonames'] is not None:
                for i in range(min(NUMCITIES, len(open_json['geonames']))):
                    if open_json['geonames'][i] and 'adminCode1' in open_json["geonames"][i] and open_json['geonames'][i]['adminCode1'] == state:
                        parsed["coordinates"] = [
                            float(open_json["geonames"][i]["lat"]), float(open_json["geonames"][i]["lng"])]
                        break
                if (isinstance(state, int)):
                        first = 0
                        first = random.randint(
                            0, min(NUMCITIES, len(open_json['geonames']) - 1))
                        parsed['coordinates'] = float(open_json['geonames'][first]["lat"]), float(
                            open_json['geonames'][first]['lng'])
        if 'coordinates' in parsed and parsed['coordinates']:
        	if parsed['coordinates'][0]<25 or parsed['coordinates'][0]>50 or parsed['coordinates'][1]>-65 or parsed['coordinates'][1]<-130:
        		parsed['coordinates'] = []
        if 'text' in data:
            parsed['text'] = data['text'].encode('ascii', 'ignore')
            if 'coordinates' in parsed:
                pprint(parsed['text'])
                target = [
                    assignPolarity(parsed['text']), list(parsed['coordinates'])]
                myStreamer.ex.append(target)
                if len(myStreamer.ex) > 10:
                    self.dumpEx()

    def on_error(self, status_code, data):
        print status_code
        # self.disconnect

    def dumpEx(self):
        f = open("testdata.txt", "w")
        json.dump(myStreamer.ex,f,indent=4,ensure_ascii=True)
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
    stream.statuses.filter(
        track="obamacare,ted cruz,politics,government,sexy,yolo",location=urllib.quote_plus("-74,40,-73,41"))
