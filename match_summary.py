import requests
import json

proxies = {
	"http": 'http://185.175.76.21:80', 
    "https": 'http://58.11.59.192:80'
}

def get_MOTM(match_id):
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	r = requests.get(url, proxies=proxies).json()
	try :
		manOfTheMatch = r["header"]["momNames"].pop()
	except:
		return None
	return manOfTheMatch

def get_match_summary(match_id):
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	state = None
	while not(state == "complete"):
		if state == "mom":  #you can remove this later
			break           # i put it rn thats all to prevent infinte loop
		r = requests.get(url, proxies=proxies).json()
		state = r["header"]["state"]	
	status = r["header"]["status"]
	return status
