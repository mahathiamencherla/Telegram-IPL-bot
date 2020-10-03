# Telegram-IPL-bot

A telegram bot that gives you instanteneous IPL match updates LIVE. 
This bot uses the PyCricbuzz library in python which takes its data from the Cricbuzz api. 
Find this bot on telegram: 
```bash
Search for "Dream11 IPL Updates" or username- @IPL_Stats_Bot
```

## Some key concepts covered:
- Object Oriented Programming
- Threading
- Domain IP Spoofing
- Web Crawling

## Few things to note:
1. Cricbuzz blocks all incoming requests from cloud servers (Heroku, AWS, GCP, or pythonanywhere)
2. We achieved a workaround by implementing Domain IP Spoofing.
3. You can get free proxy IPs from - 
```bash
https://free-proxy-list.net/
```

## Cloning this repository
```bash
https://github.com/mahathiamencherla15/Telegram-IPL-bot.git
```

## Setup locally
1. Comment the envirom lines in bot.py (this is used during deployment only)

2. Create a config.cfg file

2. In your config file, create an env variable as follows-
```bash
[credentials]
token = YOUR_TELEGRAM_TOKEN
```
3. Run the following command
```bash
python3 server.py
```
