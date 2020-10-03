from bot import telegram_chatbot
#from pycricbuzz import Cricbuzz
from Criccbuzz import *
import json
import threading
import schedule
import time
import math
from pointsTable import *
from match_summary import *

print("server.py   1")
c = Cricbuzz()
print("server.py   2")
tg_bot = telegram_chatbot("config.cfg")  

update_id = None
match_id = None
inn_final = 163
start_time = '15:30'

print("server.py   4")
matches = c.matches()
print("server.py   5")

allUserIds = [] #all subscribed users
overUpdateUserIds = [] #users who want over by over deets

t = time.time()

def refresh_match_details(state="inprogress"):
	global match_id
	for match in matches:
		if(match["srs"] == "Indian Premier League 2020" and match["mchstate"]== state):
			match_id = match["id"]
			ipl = match
			break
	return ipl		

def currUpdates():
	global inn_final
	try:
		ipl = refresh_match_details() 
	except UnboundLocalError:
		try:
			ipl = refresh_match_details("complete")
		except UnboundLocalError:
				ipl = refresh_match_details("mom")
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
	if msg == None:
		return
	elif msg == "/stop" :
		allUserIds.remove(id)
		reply = "Succesfully unsubscribed!"
	elif msg.lower() == "yes" or msg.lower() == "y" or msg == "/get_updates":
		reply = "You are going to get match details!"
		addUserId(overUpdateUserIds,id)	
	elif msg.lower() == "no" or msg.lower() == "n":	
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
		reply = "Welcome to the IPL Updates bot!\n\nUse this as a user guide:\n1. /next_match to get upcoming match details.\n2. /points_table to get updates points table.\n3. The bot is going to send you summary updates of every match. If you are prompted with a \"Do you want more match details?\" question, you can answer yes to receive over by over and wicket updates.\n4. Type \"Give me updates\" to get the current livescore. \n5. /get_updates to get over by over updates.  \n6. /stop_match_details to stop getting over by over and wicket details.\nYou can always use /stop to stop the bot.\n\nThank you!\n\n\nFind the source code on: https://github.com/mahathiamencherla15/Telegram-IPL-bot/ "	
	elif msg == "Give me updates":
		curr_time = int(time.strftime('%H%M', time.localtime(t)))
		if curr_time > 1930 and curr_time <= 2359:
			reply = currUpdates()
		else:
			reply = match_day_details(True)
	else:
		reply = "Welcome to the IPL Updates bot!\n\nUse this as a user guide:\n1. /next_match to get upcoming match details.\n2. /points_table to get updates points table.\n3. The bot is going to send you summary updates of every match. If you are prompted with a \"Do you want more match details?\" question, you can answer yes to receive over by over and wicket updates.\n4. Type \"Give me updates\" to get the current livescore. \n5. /get_updates to get over by over updates.  \n6. /stop_match_details to stop getting over by over and wicket details.\nYou can always use /stop to stop the bot.\n\nThank you!\n\n\nFind the source code on: https://github.com/mahathiamencherla15/Telegram-IPL-bot/ "	
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
	global start_time
	ipl = refresh_match_details("preview")
	if (ipl):
		team1 = ipl["team1"]["name"]
		team2 = ipl["team2"]["name"]
		start_time = ipl["start_time"]
		start_time = start_time[len(start_time)-8:len(start_time)-3]
		matchDetails = "Upcoming match: %0A"+team1+" Vs. "+team2
		if replyBackToUser:
			return (matchDetails+"%0AStarts at "+start_time)
		else:
			send_to_all(matchDetails+"%0AStarts at "+start_time)	
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
	print(1)
	global inn_final
	global start_time
	try:
		print(2)
		ipl = refresh_match_details() 
	except UnboundLocalError:
		print(3)
		try:
			ipl = refresh_match_details("complete")
		except UnboundLocalError:
			print(4)
			ipl = refresh_match_details("mom")		
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
				wickets = 0
				innings_summary(scoreCard)
		time.sleep(60)
		scoreCard = c.scorecard(match_id)	
	print("not")
	while True:
		print(5)
		match_summarry = get_match_summary(match_id)
		ipl = refresh_match_details("preview")
		start_time = ipl["start_time"]
		start_time = start_time[len(start_time)-8:len(start_time)-3]
		if match_summarry :
			print(6)
			scoreCard = c.scorecard(match_id)
			end_of_match = "The match has ended\n"+scoreCard["scorecard"][0]["batteam"] + "'s final score: " + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] + " overs\n"
			end_of_match += match_summarry
			send_to_all(end_of_match)
			match_day_details()
			set_toss_schedule()
			print(end_of_match)
			break
	#MOTM	
	print(7)
	while True:
		print(8)
		MOTM_name = get_MOTM(match_id)
		if MOTM_name:
			print(9)
			MOTM = "The man of the match is " + MOTM_name
			send_to_all(MOTM)
			print(MOTM)
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
	print("Thread Begins")
	thread1 = threading.Thread(target = get_match_details)
	thread1.start()
	return

print("server.py   6")

def set_toss_schedule():
	global start_time
	toss_time_hrs = start_time[0:2]
	toss_time_mins = int(start_time[3:5])-5
	toss_time = toss_time_hrs + ":" + str(toss_time_mins)
	# toss has to be sent 5 mins before upcoming match starts
	schedule.every().day.at(toss_time).do(toss_squad_details)
	return 

set_toss_schedule()
#no change to thread except- starting it at start_time
schedule.every().day.at(start_time).do(beginThread)
# beginThread()

print("server.py   7")

while True:
	schedule.run_pending()
	time.sleep(1)
	print ("...")
	try:
		updates = tg_bot.get_updates(offset=update_id)
		updates = updates["result"]
	except KeyError:
		print("No messages")
		pass	
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
