from bot import telegram_chatbot
from pycricbuzz import Cricbuzz
import json

c = Cricbuzz()
tg_bot = telegram_chatbot("config.cfg")  


update_id = None

matches = c.matches()

# Match stats (To be sent with "do you want match details?")
for match in matches:
	if(match["srs"] == "Indian Premier League 2020"):
		match_id = match["id"]
		ipl = match
hello = "hello"
def make_reply(msg):
	print(hello)
	if msg=="Give me updates":
		reply = json.dumps(ipl, indent = 4)
	else:
		reply = "Type: Give me updates"	
	return reply	


while True:
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
			reply = make_reply(message)
			tg_bot.send_message(reply, from_)
