import requests
import json
from proxy import *

print("match_summmary.py start")
proxy = {"https": get_working_proxy()}
print("FirstmatchSummary ",proxy)

def get_MOTM(match_id):
	print("in MOTM")
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	# r = requests.get(url, proxies=proxies).json()
	global proxy
	while True:
		print("in MOTM whileloop")
		print("in MOTM IP: ",proxy)
		try:
			r = requests.get(url, proxies=proxy).json()
			break
		except Exception:
			proxy["https"] = get_working_proxy()
	try :
		manOfTheMatch = r["header"]["momNames"].pop()
	except:
		return None
	return manOfTheMatch

def get_match_summary(match_id):
	print("in matchSUM")
	global proxy
	url = "https://mapps.cricbuzz.com/cbzios/match/{}/".format(match_id)
	state = None
	while not(state == "complete" or state == "mom"):		
		print("in matchSUM whileloop")
		while True:
			try:
				r = requests.get(url, proxies=proxy).json()
				break
			except Exception:
				proxy["https"] = get_working_proxy()
		state = r["header"]["state"]	
	status = r["header"]["status"]
	return status

