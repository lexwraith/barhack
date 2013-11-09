import json
from pprint import pprint

def json_parse(json_file):
	parsed = {}
	
	json_data = open(json_file)
	data = json.load(json_data)
	
	if ("coordinates" in data):
		if ("coordinates" in data["coordinates"]):
			parsed["coordinates"] = data["coordinates"]["coordinates"]
		else:
			parsed["coordinates"] = "[]"
	else:
			parsed["coordinates"] = "[]"
	parsed["hashtags"] = data["entities"]["hashtags"]
	parsed["screen_name"] = "@"+data["entities"]["user_mentions"][0]["screen_name"]
	parsed["text"] = data["text"]
	
	with open('parsed_tweet.json','wb') as fp:
		json.dump(parsed,fp)
	
	json_data.close()


json_parse('raw_tweet.json')			