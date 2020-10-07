from bot import telegram_chatbot
# from pycricbuzz import Cricbuzz
from Criccbuzz import *
import json
import threading
import schedule
import time
import math
from pointsTable import *

print("server.py   1")
c = Cricbuzz()
print("server.py   2")
tg_bot = telegram_chatbot("config.cfg")  

update_id = None
match_id = None
inn_final = -1
start_time = '19:30'

print("server.py   4")
matches = c.matches()
print("server.py   5")

allUserIds = [] #all subscribed users
overUpdateUserIds = [] #users who want over by over deets

t = time.time()

def refresh_match_details(state="inprogress"):
	global match_id
	ipl = None	
	print("Searching for state: ", state)
	for match in matches:	
		print(match["srs"]+"\t"+match["mchstate"])	
		if(match["srs"] == "Indian Premier League 2020" and match["mchstate"]== state):			
			match_id = match["id"]
			ipl = match	
			print("braking", ipl)		
			return ipl
	print("outside", ipl)		
	return ipl		

try:
	ipl = refresh_match_details("preview")	
	start_time = ipl["start_time"]
	start_time = start_time[len(start_time)-8:len(start_time)-3]
	print("start time has been set to ", start_time)
except Exception as e:
	print(e)
	print("did not set start_time")
	pass

def currUpdates():
	global inn_final
	global matches
	while True:
		ipl = refresh_match_details() 
		
		if ipl == None: #no match found in progress
			print("currUpdates(): no match inprogress")
			ipl = refresh_match_details("complete") 
		else:
			break #found a match in progress
		
		if ipl == None: #no match found in complete
			print("currUpdates(): no match complete")
			ipl = refresh_match_details("mom") 
		else:
			break #found a match compete
		
		if ipl == None: #no match found in mom
			print("currUpdates(): no match in mom")						
		else:
			break #found a match mom		
		matches = c.matches()
		time.sleep(60) #wait 60 seconds before searching again

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

def addUserId(userList, id):
	if id not in userList:
		userList.append(id)
	return

def removeUserId(userList, id):
	if id in userList:
		userList.remove(id)		
	return

def make_reply(msg, id):
	global start_time
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
		start_time_num = start_time.replace(":",'')
		start_time_num = int(start_time_num)
		if curr_time > start_time_num and curr_time <= 2359:
			print("going to currUpdates() ", curr_time, start_time_num)
			reply = currUpdates()
		else:
			print("going to match_day_details() ", curr_time, start_time_num)
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
	global matches	
	ipl = refresh_match_details("preview") 		
	if ipl == None: #no match found in progress
		print("No match preview available\n refreshing matches")
		matches = c.matches()	
		if replyBackToUser:
	 		return ("No match preview available")		
		
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
	global matches
	while True:
		ipl = refresh_match_details("toss") 		
		if ipl == None: #no match found in toss
			print("toss_squad_details(): no match in toss")			
			ipl = refresh_match_details("inprogress")
		else:
			break #found a match in toss
		if ipl == None:
			print("toss_squad_details(): no match in progress")	
			print("refreshing matches")
			matches = c.matches()
		else:			
			break #found a match in progress
		time.sleep(30) #wait 30 seconds before checking again
	
	while True:	
		print("Inside toss squad")
		if (ipl["team1"]["squad"] != []):
			team1 = ipl["team1"]["name"]
			team2 = ipl["team2"]["name"]
			team1Squad = "%0A".join(ipl["team1"]["squad"])
			team2Squad = "%0A".join(ipl["team2"]["squad"])
			toss = ipl["toss"].replace("elect","won the toss and elected")
			send_to_all(toss)
			send_to_all("Playing 11 for "+team1+": %0A"+team1Squad)
			send_to_all("Playing 11 for "+team2+": %0A"+team2Squad)				
			send_to_all("Do you want detailed updates of the match? (Y/N)")
			break
	return

def get_match_details():
	global matches
	try:
		print(1)
		global inn_final
		global start_time
		while True:
			ipl = refresh_match_details() 
			
			if ipl == None: #no match found in progress
				print("currUpdates(): no match inprogress")
				ipl = refresh_match_details("complete") 
			else:
				break #found a match in progress
			
			if ipl == None: #no match found in complete
				print("currUpdates(): no match complete")
				ipl = refresh_match_details("mom") 
			else:
				break #found a match compete
			
			if ipl == None: #no match found in mom
				print("currUpdates(): no match in mom")	
				print("refreshing matches")
				matches = c.matches()					
			else:
				break #found a match mom
			time.sleep(60) #wait 60 seconds before searching again

		
		scoreCard = c.scorecard(match_id)
		prev_over = 0.0
		wickets = 0
		if(inn_final == -1 and int(scoreCard["scorecard"][0]["inng_num"]) == 2):
				inn_final = int(scoreCard["scorecard"][1]["runs"]) + 1
		print("out")
		while not(float(scoreCard["scorecard"][0]["overs"]) == 20.0 and int(scoreCard["scorecard"][0]["inng_num"]) == 2):
			print("in")
			if (int(scoreCard["scorecard"][0]["runs"]) >= inn_final and int(scoreCard["scorecard"][0]["inng_num"]) == 2):
				print("exceeded target")
				break
			if (int(scoreCard["scorecard"][0]["wickets"]) == 10 and int(scoreCard["scorecard"][0]["inng_num"]) == 2):
				print("all out inn:2")
				break
			if (int(scoreCard["scorecard"][0]["wickets"]) == 10 and int(scoreCard["scorecard"][0]["inng_num"]) == 1):
				print("all out inn:1")
				wickets = 0
				innings_summary(scoreCard)
				continue
				
			if wickets != int(scoreCard["scorecard"][0]["wickets"]):
				fall_of_wickets(scoreCard)
				wickets = int(scoreCard["scorecard"][0]["wickets"])				
			print("Check is at", float(scoreCard["scorecard"][0]["overs"]))
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
			time.sleep(45)
			scoreCard = c.scorecard(match_id)	
		print("not")

		# getting match summary
		match_summary = ""
		print("Gonna get match summary")
		while True:
			print("Current match summary is ", match_summary)						
			match = c.matchinfo(match_id)
			if match['mchstate'] in ["complete", "mom"]:
				match_summary = match["status"] 
				break		
		scoreCard = c.scorecard(match_id)
		end_of_match = "The match has ended\n"+scoreCard["scorecard"][0]["batteam"] + "'s final score: " + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] + " overs\n"
		end_of_match += match_summary
		send_to_all(end_of_match)
		print("Got match summary")

		match_day_details()  #the rest is done in innings no? we could probably send upcoming match during innings break also
		
		print(end_of_match)

		matches = c.matches()
		

	except Exception as e:
		print("Error caugh by try block in get_match_details():\n ",e)
	return 	

def innings_summary(scoreCard):  	
	global matches 
	global start_time
	global inn_final
	inn_final = int(scoreCard["scorecard"][0]["runs"]) + 1	
	inn_sum = "Innings " + scoreCard["scorecard"][0]["inng_num"] + " summary:\n" + scoreCard["scorecard"][0]["runs"] + " - " + scoreCard["scorecard"][0]["wickets"] + "\n" + scoreCard["scorecard"][0]["overs"] + " overs"
	send_to_all(inn_sum)
	ipl = refresh_match_details("preview")
	while ipl ==  None:
		print("IN innings summary....couldnt find a match in preview")
		print("refreshing matches")
		matches = c.matches()
		ipl = refresh_match_details("preview")
	start_time = ipl["start_time"]
	start_time = start_time[len(start_time)-8:len(start_time)-3]
	set_toss_schedule()
	time.sleep(600)
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
	thread2 = threading.Thread(target = get_match_details)
	if(thread1.is_alive()):
		print("Thread 1 is alive")
		thread2.start()
		print("Thread 2 is starting")
	else:
		thread1.start()
	return

print("server.py   6")


def set_toss_schedule():
	global start_time
	toss_time_hrs = start_time[0:2]
	toss_time_mins = int(start_time[3:5])-5
	toss_time = toss_time_hrs + ":" + str(toss_time_mins)
	# toss has to be sent 5 mins before upcoming match starts
	print("toss time", toss_time)
	schedule.every().day.at(toss_time).do(toss_squad_details)
	return 

set_toss_schedule()
#no change to thread except- starting it at start_time
schedule.every().day.at(start_time).do(beginThread)
beginThread()

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
		continue #TypeError: string indices must be integers  ; replaced the pass in this line with continue
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
