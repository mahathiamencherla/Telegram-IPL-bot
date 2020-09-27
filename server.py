from bot import telegram_chatbot
from pycricbuzz import Cricbuzz
import json

import schedule
import time

c = Cricbuzz()
tg_bot = telegram_chatbot("config.cfg")  

update_id = None
match_id = None

yesFlag = False

matches = c.matches()

allUserIds = [] #all subscribed users
overUpdateUserIds = [] #users who want over by over deets

# Match stats (To be sent with "do you want match details?")
def refresh_match_details():
	global match_id
	for match in matches:
		if(match["srs"] == "Indian Premier League 2020"):
			match_id = match["id"]
			ipl = match
	return ipl		

ipl = refresh_match_details() 
liveScore = c.livescore(match_id)

def addUserId(userList, id):
	if id not in userList:
		userList.append(id)

def removeUserId(userList, id):
	if id in userList:
		userList.remove(id)		

def make_reply(msg, id):
	global yesFlag
	if msg=="Give me updates":
		reply = json.dumps(ipl, indent = 4)
	elif msg == "/stop" :
		allUserIds.remove(id)
		reply = "Succesfully unsubscribed!"
	elif msg == "Yes" or msg == "YES" or msg == "yes" or msg == "Y":
		reply = "You are going to get match details!"
		addUserId(overUpdateUserIds,id)
		yesFlag = True
	elif msg == "no" or msg == "NO" or msg == "No" or msg == "N":	
		reply = "Okay, no match details."
	elif msg == "/stop-match-details":
		removeUserId(overUpdateUserIds,id)
		reply = "You won't be getting detailed updates for this match anymore."	
	elif msg == "/help":
		reply = "Welcome to the IPL Updates bot.\n Use this as a user guide:\n1. /next-match to get upcoming match details.\n2. /points-table to get updates points table.\nThe bot is going to send you summary updates of every match. If you are prompted with a \"Do you want more match details?\" question, you can answer yes to receive over by over and wicket updates.\nUse /stop-match-details to stop getting over by over and wicket details.\nYou can always use /stop to stop the bot.\nThank you!\nFind the source code on: https://github.com/mahathiamencherla15/Telegram-IPL-bot/ "	
	else:
		reply = "Type: Give me updates"	
	return reply	

def send_to_all(msg):
	for id in allUserIds:
		tg_bot.send_message(msg, id)

def match_day_details():
	ipl = refresh_match_details()
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
	send_to_all("Do you want detailed updates of the match? (Y/N)")

def get_match_details(liveScore):
	return 



def match_summary():  #call when mchstate changes to mom
	return

schedule.every().day.at("00:00").do(match_day_details)
schedule.every().day.at("19:38").do(toss_squad_details)

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
