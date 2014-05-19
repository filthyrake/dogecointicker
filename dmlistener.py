# Dogecoin Ticker Twitter Bot
# Written by Damen Knight
# Copyright 2014

import tweepy, time, sys
import json
import urllib2
import os


CONSUMER_KEY = '<consumer_key>'
CONSUMER_SECRET = '<consumer_secret>'
ACCESS_KEY = '<access_key>'
ACCESS_SECRET = '<access_secret>'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

messages = api.direct_messages()

for message in messages:
	if message.text.lower() == "cryptsy":
		filename=open('/path/to/cryptsyvalue.txt','r')
		f=filename.readline()
		filename.close()
		reply = f
		user = message.sender_id
		api.send_direct_message(user, text=reply)
	if message.text.lower() == "vircurex":
                filename=open('/path/to/vircurexvalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)
        if message.text.lower() == "bter":
                filename=open('/path/to/btervalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)
        if (message.text.lower() == "coins-e") or (message.text.lower() == "coinse"):
                filename=open('/path/to/coinsevalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)
        if message.text.lower() == "mintpal":
                filename=open('/path/to/mintpalvalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)



#delete all existing DMs
for message in messages:
	api.destroy_direct_message(message.id)

