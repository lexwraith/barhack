import json
import nltk
import urllib2
import subprocess
import unirest
import ast
from pprint import pprint

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
	response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",headers={"X-Mashape-Authorization": "q9WreMnPjMW5iL3yNpbnM4jwRmVr6Sbu"},params={"text": text,"language": "english"})
  	sentiment = response.body
  	maxval = 0
  	maxpol = ''
  	for pol in sentiment["probability"]:
  		value = sentiment["probability"][pol]
  		if (value >= maxval):
  			maxval = value
  			maxpol = pol
  	return [maxpol,maxval]

def jsonParse(json_file):
	parsed = {}
	json_data = open(json_file)
	data = json.load(json_data)
	NUMCITIES = 10
	
	if ("coordinates" in data and "coordinates" in data["coordinates"]):
			parsed["coordinates"] = data["coordinates"]["coordinates"]
	else:
		state = 0
		location = data["user"]["location"]
		
		# MIKE! COPY FROM HERE...
		if (',' in location):
			location = location.partition(',')
			if (len(location) == 3):
				city = location[0].strip().lower().replace(' ','_')
				if (len(location[2].strip()) == 2):
					state = location[2].strip().upper()
				elif (location[2].strip().upper() in stateCodes):
					state = stateCodes[location[2].strip().upper()]
		else:
			city = location.lower().replace(' ','_')
		# ... TO HERE!!!! And the stateCodes dictionary ;)
		
		catch_json = urllib2.urlopen('http://api.geonames.org/searchJSON?q='+city+'&maxRows='+str(NUMCITIES)+'&username=cmiller0330')
		open_json = ast.literal_eval(catch_json.read())
		
		i = 0;
		while (i<NUMCITIES):
			if (len(open_json["geonames"])>0):
				if (type(state) == int):
					parsed["coordinates"] = [float(open_json["geonames"][0]["lat"]),float(open_json["geonames"][0]["lng"])]
					break
				elif (open_json["geonames"][i] and "adminCode1" in open_json["geonames"][i] and open_json["geonames"][i]["adminCode1"] == state):
					parsed["coordinates"] = [float(open_json["geonames"][i]["lat"]),float(open_json["geonames"][i]["lng"])]
					break
				else:
					parsed["coordinates"] = []
			else:
				parsed["coordinates"] = []
				break
			i+=1
			
	parsed["hashtags"] = data["entities"]["hashtags"]
	parsed["screen_name"] = "@"+data["entities"]["user_mentions"][0]["screen_name"]
	parsed["text"] = data["text"]
	parsed["polarity"] = assignPolarity(parsed["text"])
	
	with open('parsed_tweet.json','wb') as fp:
		json.dump(parsed,fp)
	json_data.close()

jsonParse('raw_tweet.json')			