# Dogecoin Ticker Twitter Bot
# Written by Damen Knight
# Copyright 2014

import tweepy, time, sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/path/to/appconfig")

argfile = str(sys.argv[1])

CONSUMER_KEY = config.get('appconfig','consumer_key')
CONSUMER_SECRET = config.get('appconfig','consumer_secret')
ACCESS_KEY = config.get('appconfig','access_key')
ACCESS_SECRET = config.get('appconfig','access_secret')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

filename=open(argfile,'r')
f=filename.readlines()
filename.close()
 
for line in f:
	api.update_status(status=line)
	time.sleep(30)#Tweet every 30 seconds
