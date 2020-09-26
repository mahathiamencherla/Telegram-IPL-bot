#telegram Bot
import json
from pycricbuzz import Cricbuzz

c = Cricbuzz()

matches = c.matches()

# Match stats (To be sent with "do you want match details?")
for match in matches:
	if(match["srs"] == "Indian Premier League 2020"):
		match_id = match["id"]
		ipl = match

# print(json.dumps(ipl, indent = 4))

# this is for live score updates. (when score["overs"] is a whole number)
liveScore = c.livescore(match_id)

print(json.dumps(liveScore, indent = 4))

# summary after every innings (when score["overs"] is 20 and inns_num is 1 and 2) 
scoreCard = c.scorecard(match_id)

print(json.dumps(scoreCard, indent = 4))

