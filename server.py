from bot import telegram_chatbot
from pycricbuzz import Cricbuzz
import json

import schedule
import time

c = Cricbuzz()
tg_bot = telegram_chatbot("config.cfg")  

update_id = None

matches = c.matches()

allUserIds = [] #all subscribed users
overUpdateUserIds = [] #users who want over by over deets

# Match stats (To be sent with "do you want match details?")
def refresh_match_details():
	for match in matches:
		if(match["srs"] == "Indian Premier League 2020"):
			match_id = match["id"]
			if match["mchstate"] == "preview" :
				ipl = match
			else:
				completed_ipl = match

refresh_match_details() 

def addUserId(userList, id):
	if id not in userList:
		userList.append(id)

def make_reply(msg, id):
	print("hello")
	if msg=="Give me updates":
		reply = json.dumps(ipl, indent = 4)
	elif msg == "/stop" :
		allUserIds.remove(id)
		reply = "Succesfully unsubscribed!"
	else:
		reply = "Type: Give me updates"	
	return reply	

def send_to_all(msg):
	for id in allUserIds:
		tg_bot.send_message(msg, id)

def match_day_details():
	refresh_match_details()
	team1 = ipl["team1"]["name"]
	team2 = ipl["team2"]["name"]
	toss = ipl["toss"]
	matchDetails = "Upcoming match: %0A"+team1+" Vs. "+team2
	send_to_all(matchDetails+"%0AStarts at 19:30(ist)")	

def toss_squad_details():
	team1 = ipl["team1"]["name"]
	team2 = ipl["team2"]["name"]
	team1Squad = "%0A".join(ipl["team1"]["squad"])
	team2Squad = "%0A".join(ipl["team2"]["squad"])
	toss = ipl["toss"].replace("elect","won the toss and elected")
	send_to_all(toss)
	send_to_all("Playing 11 for "+team1+": %0A"+team1Squad)
	send_to_all("Playing 11 for "+team2+": %0A"+team2Squad)	
	send_to_all("Do you detailed over updates(Y/N)")

def match_summary():  #call when mchstate changes to mom
	return

schedule.every().day.at("00:00").do(match_day_details)
schedule.every().day.at("19:15").do(toss_squad_details)

while True:
	schedule.run_pending()
	time.sleep(1)
	print ("...")
	updates = tg_bot.get_updates(offset=update_id)
	updates = updates["result"]
	if updates:
		for item in updates:
			update_id = item["update_id"]
			try: 
				message = item["message"]["text"]
			except:
				message = None
			from_ = item["message"]["from"]["id"]
			addUserId(allUserIds, from_)
			reply = make_reply(message, from_)
			tg_bot.send_message(reply, from_)					
