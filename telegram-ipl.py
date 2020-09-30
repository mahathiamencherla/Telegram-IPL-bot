#telegram Bot
import json
# from pycricbuzz import Cricbuzz
from Criccbuzz import *

c = Cricbuzz()
match_id = None
matches = c.matches()

# Match stats (To be sent with "do you want match details?")
for match in matches:
	if(match["srs"] == "Indian Premier League 2020" ):
		match_id = match["id"]
		ipl = match	
		# print(json.dumps(match, indent = 4))	
		break	

# print(json.dumps(ipl, indent = 4))

# this is for live score updates. (when score["overs"] is a whole number)
# liveScore = c.livescore(match_id)

# print(json.dumps(liveScore, indent = 4))

# # summary after every innings (when score["overs"] is 20 and inns_num is 1 and 2) 
scoreCard = c.scorecard(match_id)
print(json.dumps(scoreCard, indent = 4))
#print(json.dumps(scoreCard["scorecard"][0], indent = 4))	
#print(json.dumps(scoreCard["scorecard"][1], indent = 4))	
# print(scoreCard["scorecard"][1]["runs"])
#print(scoreCard["scorecard"][::-1]["runs"])

# match_info = c.matchinfo(match_id)
# print(json.dumps(match_info, indent = 4))
# we need MOTM etc
#update once wicket happens



def fall_of_wickets():
	fallen_batsman = scoreCard["scorecard"][0]["fall_wickets"].pop()
	msg = fallen_batsman['name']+" is out!\n"+fallen_batsman['score']+" - "+fallen_batsman['wkt_num']+"\n"+fallen_batsman["overs"]+" overs"
	print(msg)

def innings_summary():  
	global scoreCard		
	inn_sum = "Innings " + scoreCard["scorecard"][0]["inng_num"] + " summary:\n" + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] +" overs"
	print(inn_sum)	

# print(int(scoreCard["scorecard"][0]["wickets"]), type(int(scoreCard["scorecard"][0]["wickets"])))
	