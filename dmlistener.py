import tweepy, time, sys
import json
import urllib2
import os

import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/path/to/appconfig")

CONSUMER_KEY = config.get('appconfig','consumer_key')
CONSUMER_SECRET = config.get('appconfig','consumer_secret')
ACCESS_KEY = config.get('appconfig','access_key')
ACCESS_SECRET = config.get('appconfig','access_secret')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

messages = api.direct_messages()

for message in messages:
	if message.text.lower().find("cryptsy") != -1:
		filename=open('/path/to/cryptsyvalue.txt','r')
		f=filename.readline()
		filename.close()
		reply = f
		user = message.sender_id
		api.send_direct_message(user, text=reply)
	if message.text.lower().find("vircurex") != -1:
                filename=open('/path/to/vircurexvalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)
        if message.text.lower().find("bter") != -1:
                filename=open('/path/to/btervalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)
        if (message.text.lower().find("coins-e") != -1) or (message.text.lower().find("coinse") != -1):
                filename=open('/path/to/coinsevalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)
        if message.text.lower().find("mintpal") != -1:
                filename=open('/path/to/mintpalvalue.txt','r')
                f=filename.readline()
                filename.close()
                reply = f
                user = message.sender_id
                api.send_direct_message(user, text=reply)



#delete all existing DMs
for message in messages:
	api.destroy_direct_message(message.id)

