import requests
import json


def get_MOTM(match_id):
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	r = requests.get(url).json()
	try :
		manOfTheMatch = r["header"]["momNames"].pop()
	except:
		return None
	return manOfTheMatch

def get_match_summary(match_id):
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	r = requests.get(url).json()
	try:
		status = r["header"]["status"]
	except:
		return None
	return status