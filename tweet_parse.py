import json
import urllib2
import ast
from pprint import pprint

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
				city = location[0].strip().lower().replace(' ','_')
				if (len(location[2].strip()) == 2):
					state = location[2].strip().upper()
				else:
					state = location[2].strip().upper()[0:2]
		else:
			city = location.lower().replace(' ','_')
		
		print(city, state)
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
	
	with open('parsed_tweet.json','wb') as fp:
		json.dump(parsed,fp)
	json_data.close()

json_parse('raw_tweet.json')			