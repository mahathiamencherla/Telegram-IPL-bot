import requests
import json


def get_MOTM(match_id):
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	r = requests.get(url).json()
	manOfTheMatch = r["header"]["momNames"].pop()
	return manOfTheMatch

def get_match_summary(match_id):
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	r = requests.get(url).json()
	status = r["header"]["status"]
	return status

print(get_match_summary("30375"))