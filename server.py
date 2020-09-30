from bot import telegram_chatbot
# from pycricbuzz import Cricbuzz
from Criccbuzz import *
import json
import threading
import schedule
import time
import math
from pointsTable import *

c = Cricbuzz()
tg_bot = telegram_chatbot("config.cfg")  

update_id = None
match_id = None
inn_final = 163
yesFlag = False

matches = c.matches()

allUserIds = [] #all subscribed users
overUpdateUserIds = [] #users who want over by over deets

t = time.time()

def refresh_match_details(state="inprogress"):
	global match_id
	for match in matches:
		if(match["srs"] == "Indian Premier League 2020" and match["mchstate"]== state):
			match_id = match["id"]
			ipl = match
	return ipl		

def currUpdates():
	global inn_final
	ipl = refresh_match_details() 
	scoreCard = c.scorecard(match_id)
	team1 = ipl["team1"]["name"]
	team2 = ipl["team2"]["name"]
	over_update = team1+" Vs. "+team2+"\n"
	over_update += "Innings number: " + scoreCard["scorecard"][0]["inng_num"] + "\n"
	over_update += scoreCard["scorecard"][0]["batteam"] + " are batting!\n" + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] + " overs\n"
	batcard = scoreCard["scorecard"][0]["batcard"]
	for batsman in batcard:
		if(batsman["dismissal"] == "batting"):
			over_update += 	batsman["name"] + " - " + batsman["runs"] + "(" + batsman["balls"] + ")\n"
	if(int(scoreCard["scorecard"][0]["inng_num"]) == 2):
		curr_balls = float(scoreCard["scorecard"][0]["overs"])
		over_update += str((inn_final - int(scoreCard["scorecard"][0]["runs"]))) + " runs required from "	+ str(int(120-((math.floor(curr_balls)*6)+(curr_balls*10)%10))) +" balls."	

	return over_update


# scoreCard = c.scorecard(match_id)

def addUserId(userList, id):
	if id not in userList:
		userList.append(id)
	return

def removeUserId(userList, id):
	if id in userList:
		userList.remove(id)		
	return

def make_reply(msg, id):
	global yesFlag
	if msg == None:
		return
	elif msg == "/stop" :
		allUserIds.remove(id)
		reply = "Succesfully unsubscribed!"
	elif msg.lower() == "yes" or msg.lower() == "Y" or msg == "/get_updates":
		reply = "You are going to get match details!"
		addUserId(overUpdateUserIds,id)
		yesFlag = True		
	elif msg.lower() == "no" or msg.lower() == "N":	
		reply = "Okay, no match details."
	elif msg == "/points_table":	
		table = getPointsTable()
		reply = pointsTableParser(table)
	elif msg == "/stop_match_details":
		removeUserId(overUpdateUserIds,id)
		reply = "You won't be getting detailed updates for this match anymore."	
	elif msg == "/next_match":
		reply = match_day_details(True)
	elif msg == "/help":
		reply = "Welcome to the IPL Updates bot!\n\nUse this as a user guide:\n1. /next_match to get upcoming match details.\n2. /points_table to get updates points table.\n3. The bot is going to send you summary updates of every match. If you are prompted with a \"Do you want more match details?\" question, you can answer yes to receive over by over and wicket updates.\n4. Type \"Give me updates\" to get the current livescore. \n5. /get_updates to get over by over updates  \n6. /stop_match_details to stop getting over by over and wicket details.\nYou can always use /stop to stop the bot.\n\nThank you!\n\n\nFind the source code on: https://github.com/mahathiamencherla15/Telegram-IPL-bot/ "	
	elif msg == "Give me updates":
		curr_time = int(time.strftime('%H%M', time.gmtime(t)))
		if curr_time > 1400 and curr_time <= 1829:
			reply = currUpdates()
		else:
			reply = match_day_details(True)
	else:
		reply = "Welcome to the IPL Updates bot!\n\nUse this as a user guide:\n1. /next_match to get upcoming match details.\n2. /points_table to get updates points table.\n3. The bot is going to send you summary updates of every match. If you are prompted with a \"Do you want more match details?\" question, you can answer yes to receive over by over and wicket updates.\n4. Type \"Give me updates\" to get the current livescore. \n5. /get_updates to get over by over updates  \n6. /stop_match_details to stop getting over by over and wicket details.\nYou can always use /stop to stop the bot.\n\nThank you!\n\n\nFind the source code on: https://github.com/mahathiamencherla15/Telegram-IPL-bot/ "	
	return reply	

def send_to_all(msg):
	for id in allUserIds:
		tg_bot.send_message(msg, id)
	return

def send_over_updates(msg):
	if overUpdateUserIds == []:
		return
	for id in overUpdateUserIds:
		tg_bot.send_message(msg, id)
	return

def match_day_details(replyBackToUser = False):
	ipl = refresh_match_details("preview")
	team1 = ipl["team1"]["name"]
	team2 = ipl["team2"]["name"]
	matchDetails = "Upcoming match: %0A"+team1+" Vs. "+team2
	if replyBackToUser:
		return (matchDetails+"%0AStarts at 19:30(ist)")
	else:
		send_to_all(matchDetails+"%0AStarts at 19:30(ist)")	
		return

def toss_squad_details():
	ipl = refresh_match_details("preview")
	team1 = ipl["team1"]["name"]
	team2 = ipl["team2"]["name"]
	team1Squad = "%0A".join(ipl["team1"]["squad"])
	team2Squad = "%0A".join(ipl["team2"]["squad"])
	toss = ipl["toss"].replace("elect","won the toss and elected")
	send_to_all(toss)
	send_to_all("Playing 11 for "+team1+": %0A"+team1Squad)
	send_to_all("Playing 11 for "+team2+": %0A"+team2Squad)	
	send_to_all("Do you want detailed updates of the match? (Y/N)")
	return

def get_match_details():
	global inn_final
	ipl = refresh_match_details()	
	scoreCard = c.scorecard(match_id)
	prev_over = 0.0
	wickets = 0
	while not(float(scoreCard["scorecard"][0]["overs"]) == 20.0 and int(scoreCard["scorecard"][0]["inng_num"]) == 2) :
		if wickets != int(scoreCard["scorecard"][0]["wickets"]):
			fall_of_wickets(scoreCard)
			wickets = int(scoreCard["scorecard"][0]["wickets"])
		if(float(scoreCard["scorecard"][0]["overs"]) == 20.0 and int(scoreCard["scorecard"][0]["inng_num"]) == 1):
			inn_final = int(scoreCard["scorecard"][0]["runs"]) + 1
		if(inn_final == None):
			inn_final = scoreCard["scorecard"][1]["runs"]
		if float(scoreCard["scorecard"][0]["overs"]).is_integer() and prev_over != float(scoreCard["scorecard"][0]["overs"]):			
			prev_over = float(scoreCard["scorecard"][0]["overs"])			
			over_update = scoreCard["scorecard"][0]["batteam"] + " are batting!\n" + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] + " overs\n"
			batcard = scoreCard["scorecard"][0]["batcard"]
			for batsman in batcard:
				if(batsman["dismissal"] == "batting"):
					over_update += 	batsman["name"] + " - " + batsman["runs"] + "(" + batsman["balls"] + ")\n"
			if(int(scoreCard["scorecard"][0]["inng_num"]) == 2):
				curr_balls = float(scoreCard["scorecard"][0]["overs"])
				over_update += str((inn_final - int(scoreCard["scorecard"][0]["runs"]))) + " runs required from "	+ str(int(120-((math.floor(curr_balls)*6)+(curr_balls*10)%10))) +" balls."	
			send_over_updates(over_update)			
			if(float(scoreCard["scorecard"][0]["overs"]) == 20.0):
				innings_summary(scoreCard)
		time.sleep(60)
		scoreCard = c.scorecard(match_id)
	#match end
	while True:
		if get_match_summary(match_id):
			scoreCard = c.scorecard(match_id)
			end_of_match = "The match has ended\n"+scoreCard["scorecard"][0]["batteam"] + "'s Final score:" + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] + " overs\n"
			end_of_match += get_match_summary(match_id)
			send_to_all(end_of_match)
			break
	#MOTM	
	while True:
		if get_MOTM(match_id):
			MOTM = "The man of the match is " + "get_MOTM(match_id)"
			send_to_all(MOTM)
			break
	return 

def innings_summary(scoreCard):  	
	inn_sum = "Innings " + scoreCard["scorecard"][0]["inng_num"] + " summary:\n" + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] + " overs"
	send_to_all(inn_sum)
	time.sleep(900)
	return

def fall_of_wickets(scoreCard):
	fallen_batsman = scoreCard["scorecard"][0]["fall_wickets"].pop()
	batcard = scoreCard["scorecard"][0]["batcard"]
	for batsman in batcard:
		if batsman["name"] == fallen_batsman['name']:
			dismissal = batsman["dismissal"]
	msg = fallen_batsman['name'] + " is out!\n" + dismissal + "\n" + fallen_batsman['score'] + " - " + fallen_batsman['wkt_num'] + "\n" + fallen_batsman["overs"] + " overs" 
	send_over_updates(msg)	
	return

def beginThread() :	
	thread1 = threading.Thread(target = get_match_details)
	thread1.start()
	return

schedule.every().day.at("00:00").do(match_day_details)
schedule.every().day.at("19:20").do(toss_squad_details)
schedule.every().day.at("19:30").do(beginThread)
#beginThread()

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
