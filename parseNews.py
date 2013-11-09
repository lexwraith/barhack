import urllib2
import json
from pprint import pprint

def parseNews():
	raw_data = urllib2.urlopen('http://api.nytimes.com/svc/news/v3/content/all/all/1?api-key=0876EADA373630F6DCE66728C4A9910E:1:68387525')
	title_data = json.loads(raw_data.read())
	storage_array = []
	i = 0
	for i in title_data["results"]:
		title_words = i["title"].split()
		sub_words = i["abstract"].strip(".,?!:;'()").split()
		for titword in title_words:
			if len(titword) > 2:
				storage_array.append(titword)
		for subword in sub_words:
			if len(subword) > 2:
				storage_array.append(subword)
	return set(storage_array)