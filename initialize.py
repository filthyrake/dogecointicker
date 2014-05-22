# Dogecoin Ticker Twitter Bot
# Written by Damen Knight
# Copyright 2014

from __future__ import print_function
import json
import urllib2
import MySQLdb
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/path/to/appconfig")
username = config.get('dbconfig','dbuser')
password = config.get('dbconfig','dbpass')
dbname = config.get('dbconfig','dbname')
dbhost = config.get('dbconfig','host')
exchanges = config.get('appconfig','exchanges')
exchanges = exchanges.split(',')

db = MySQLdb.connect(dbhost, username, password, dbname)
cursor = db.cursor()

#if the tables dont already exist, create them and pre-populate with exchanges
createtable = """CREATE TABLE IF NOT EXISTS exchanges (
		 URL varchar(255) NOT NULL,
		 DAYVALUE varchar(255) NOT NULL,
		 CURRENTVALUE varchar(255) NOT NULL,
		 VOLUME varchar(255) NOT NULL,
		 NAME varchar(255) NOT NULL,
		 PRIMARY KEY (NAME) ) """
cursor.execute(createtable) 

for exchange in exchanges:
	createrows = "INSERT INTO exchanges(URL, DAYVALUE, CURRENTVALUE, VOLUME, NAME) VALUES (%s,%s,%s,%s,%s)"
	cursor.execute(createrows, ("http://", "0.0", "0.0", "0.0", exchange))
		

initurls = "UPDATE exchanges SET URL = %s WHERE NAME = %s"
initdayvalues = "UPDATE exchanges SET DAYVALUE = %s WHERE NAME = %s"
initcurrentvalues = "UPDATE exchanges SET CURRENTVALUE = %s WHERE NAME = %s"
initvolume = "UPDATE exchanges SET VOLUME = %s WHERE NAME = %s"


cryptsyresponse = urllib2.urlopen('http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132')
cryptsydata = json.load(cryptsyresponse)

#set the URL for cryptsy
cursor.execute(initurls, ("http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132","cryptsy"))

#set the DAYVALUE and CURRENTVALUE for cryptsy
cursor.execute(initdayvalues, (cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"], "cryptsy"))
cursor.execute(initcurrentvalues, (cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"], "cryptsy"))

#set the VOLUME for cryptsy
cursor.execute(initvolume, (cryptsydata["return"]["markets"]["DOGE"]["volume"], "cryptsy"))

vircurexurl = 'https://api.vircurex.com/api/get_highest_bid.json?base=DOGE&alt=BTC'

#set the URL for vircurex
cursor.execute(initurls, (vircurexurl, "vircurex"))

vircurexvolurl = 'https://api.vircurex.com/api/get_volume.json?base=DOGE&alt=BTC'
vircurexreq = urllib2.Request(vircurexurl, headers={"User-Agent" : "DogeCoin Ticker"})
vircurexvolreq = urllib2.Request(vircurexvolurl, headers={"User-Agent" : "DogeCoin Ticker"})
vircurexresponse = urllib2.urlopen(vircurexreq)
vircurexvolresponse = urllib2.urlopen(vircurexvolreq)
vircurexdata = json.load(vircurexresponse)

#set the DAYVALUE and CURRENTVALUE for vircurex
cursor.execute(initdayvalues, (vircurexdata["value"], "vircurex"))
cursor.execute(initcurrentvalues, (vircurexdata["value"], "vircurex"))

vircurexvoldata = json.load(vircurexvolresponse)

#set the VOLUME for vircurex
cursor.execute(initvolume, (vircurexvoldata["value"], "vircurex"))

coinseresponse = urllib2.urlopen('https://www.coins-e.com/api/v2/market/DOGE_BTC/depth/')

#set the URL for coins-e
cursor.execute(initurls, ("https://www.coins-e.com/api/v2/market/DOGE_BTC/depth/", "coins-e"))

coinsedata = json.load(coinseresponse)

#set the DAYVALUE and CURRENTVALUE for coins-e
cursor.execute(initdayvalues, (coinsedata["bid"], "coins-e"))
cursor.execute(initcurrentvalues, (coinsedata["bid"], "coins-e"))

#set the VOLUME for coins-e
cursor.execute(initvolume,(coinsedata["total_ask_q"], "coins-e"))

bterurl='http://data.bter.com/api/1/ticker/doge_btc'

#set the URL for BTER
cursor.execute(initurls, ("http://data.bter.com/api/1/ticker/doge_btc", "bter"))

bterreq = urllib2.Request(bterurl, headers={"User-Agent" : "DogeCoin Ticker"})
bterresponse = urllib2.urlopen(bterreq)
bterdata = json.load(bterresponse)

#set the DAYVALUE and CURRENTVALUE for bter
cursor.execute(initdayvalues, (bterdata["last"], "bter"))
cursor.execute(initcurrentvalues, (bterdata["last"], "bter"))

#set the VOLUME for bter
cursor.execute(initvolume, (bterdata["vol_doge"], "bter"))

mintpalresponse = urllib2.urlopen('https://api.mintpal.com/v1/market/stats/DOGE/BTC')

#set the URL for mintpal
cursor.execute(initurls, ("https://api.mintpal.com/v1/market/stats/DOGE/BTC", "mintpal"))

mintpaldata = json.load(mintpalresponse)

#set the DAYVALUE and CURRENTVALUE for mintpal
cursor.execute(initdayvalues, (mintpaldata[0]["last_price"], "mintpal"))
cursor.execute(initcurrentvalues, (mintpaldata[0]["last_price"], "mintpal"))

#We dont know how to get the VOLUME for mintpal currently, so not initializing this beyond the starting "0.0"

db.close()

f = open('/path/to/cryptsytrend.txt','w')
f.write(cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"])
f.close()
f = open('/path/to/vircurextrend.txt','w')
f.write(vircurexdata["value"])
f.close()
f = open('/path/to/coinsetrend.txt','w')
f.write(coinsedata["bid"])
f.close()
f = open('/path/to/btertrend.txt','w')
f.write(bterdata["last"])
f.close()
f = open('/path/to/mintpaltrend.txt','w')
f.write(mintpaldata[0]["last_price"])
f.close()
