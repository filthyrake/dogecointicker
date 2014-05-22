# Dogecoin Ticker Twitter Bot
# Written by Damen Knight
# Copyright 2014

import tweepy, time, sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/path/to/appconfig")

CONSUMER_KEY = config.get('appconfig','consumer_key')
CONSUMER_SECRET = config.get('appconfig','consumer_secret')
ACCESS_KEY = config.get('appconfig','access_key')
ACCESS_SECRET = config.get('appconfig','access_secret')

argfile = str(sys.argv[1])

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

filename=open(argfile,'r')
f=filename.readlines()
filename.close()

for status in tweepy.Cursor(api.user_timeline).items():
	api.destroy_status(status.id)
 
for line in f:
	api.update_status(line)
	time.sleep(30)#Tweet every 30 seconds
