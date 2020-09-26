from bot import telegram_chatbot

tg_bot = telegram_chatbot("config.cfg")  
update_id = None

def make_reply(msg):
	if msg is not None:
		reply = "Hey! This is to test our bot"
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
