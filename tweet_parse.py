import json
import urllib2
import ast
from pprint import pprint

def json_parse(json_file):
	parsed = {}
	json_data = open(json_file)
	data = json.load(json_data)
	
	if ("coordinates" in data and "coordinates" in data["coordinates"]):
			parsed["coordinates"] = data["coordinates"]["coordinates"]
	else:
		city = data["user"]["location"].split()[0].strip(',').lower()
		catch_json = urllib2.urlopen('http://api.geonames.org/searchJSON?q='+city+'&maxRows=1&username=cmiller0330')
		open_json = ast.literal_eval(catch_json.read())
		parsed["coordinates"] = [open_json["geonames"][0]["lat"],open_json["geonames"][0]["lng"]]
		
	parsed["hashtags"] = data["entities"]["hashtags"]
	parsed["screen_name"] = "@"+data["entities"]["user_mentions"][0]["screen_name"]
	parsed["text"] = data["text"]
	
	with open('parsed_tweet.json','wb') as fp:
		json.dump(parsed,fp)
	json_data.close()

json_parse('raw_tweet.json')			