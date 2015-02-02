# Dogecoin Ticker Twitter Bot
# Written by Damen Knight
# Copyright 2014
from __future__ import print_function
import json
import urllib2
import os
import MySQLdb
import ConfigParser
import ctypes
libc = ctypes.cdll.LoadLibrary('libc.so.6')
res_init = libc.__res_init

res_init()

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

cryptsyresponse = urllib2.urlopen('http://pubapi.cryptsy.com/api.php?method=singlemarketdata&marketid=132')
cryptsydata = json.load(cryptsyresponse)
vircurexurl = 'https://api.vircurex.com/api/get_highest_bid.json?base=DOGE&alt=BTC'
vircurexvolurl = 'https://api.vircurex.com/api/get_volume.json?base=DOGE&alt=BTC'
vircurexreq = urllib2.Request(vircurexurl, headers={"User-Agent" : "DogeCoin Ticker"})
vircurexvolreq = urllib2.Request(vircurexvolurl, headers={"User-Agent" : "DogeCoin Ticker"})
vircurexresponse = urllib2.urlopen(vircurexreq)
vircurexvolresponse = urllib2.urlopen(vircurexvolreq)
vircurexdata = json.load(vircurexresponse)
vircurexvoldata = json.load(vircurexvolresponse)
coinseresponse = urllib2.urlopen('https://www.coins-e.com/api/v2/market/DOGE_BTC/depth/')
coinsedata = json.load(coinseresponse)
bterurl='http://data.bter.com/api/1/ticker/doge_btc'
bterreq = urllib2.Request(bterurl, headers={"User-Agent" : "DogeCoin Ticker"})
bterresponse = urllib2.urlopen(bterreq)
bterdata = json.load(bterresponse)
coinbaseresponse = urllib2.urlopen('https://coinbase.com/api/v1/prices/buy')
coinbasedata = json.load(coinbaseresponse)

#Get the initial day values from the DB
dayvalue = "SELECT DAYVALUE FROM exchanges WHERE NAME = %s"
cursor.execute(dayvalue, ("cryptsy"))
cryptsydayvalue = cursor.fetchone()[0]

cursor.execute(dayvalue, ("vircurex"))
vircurexdayvalue = cursor.fetchone()[0]

cursor.execute(dayvalue, ("coins-e"))
coinsedayvalue = cursor.fetchone()[0]

cursor.execute(dayvalue, ("bter"))
bterdayvalue = cursor.fetchone()[0]

#Set Current Values in the DB
currentvaluesql = "UPDATE exchanges SET CURRENTVALUE = %s WHERE NAME = %s"
cursor.execute(currentvaluesql, (cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"], "cryptsy"))
cursor.execute(currentvaluesql, (vircurexdata["value"], "vircurex"))
cursor.execute(currentvaluesql, (coinsedata["bid"], "coins-e"))
cursor.execute(currentvaluesql, (bterdata["last"], "bter"))

#Set Current Volumes in the DB
volumesql = "UPDATE exchanges SET VOLUME = %s WHERE NAME = %s"
cursor.execute(volumesql, (cryptsydata["return"]["markets"]["DOGE"]["volume"], "cryptsy"))
cursor.execute(volumesql, (vircurexvoldata["value"], "vircurex"))
cursor.execute(volumesql, (coinsedata["total_ask_q"], "coins-e"))
cursor.execute(volumesql, (bterdata["vol_doge"], "bter"))

db.close()

if cryptsydayvalue < cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]:
	cryptsytrend = "up"
if cryptsydayvalue == cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]:
	cryptsytrend = "stable"
if cryptsydayvalue > cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]:
	cryptsytrend = "down"

if vircurexdayvalue < vircurexdata["value"]:
	vircurextrend = "up"
if vircurexdayvalue == vircurexdata["value"]:
	vircurextrend = "stable"
if vircurexdayvalue > vircurexdata["value"]:
	vircurextrend = "down"

if coinsedayvalue < coinsedata["bid"]:
	coinsetrend = "up"
if coinsedayvalue == coinsedata["bid"]:
	coinsetrend = "stable"
if coinsedayvalue > coinsedata["bid"]:
	coinsetrend = "down"

if bterdayvalue < bterdata["last"]:
	btertrend = "up"
if bterdayvalue == bterdata["last"]:
	btertrend = "stable"
if bterdayvalue > bterdata["last"]:
	btertrend = "down"

lowest = cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]
if vircurexdata["value"] < lowest:
	lowest = vircurexdata["value"]
if coinsedata["bid"] < lowest:
	lowest = coinsedata["bid"]
if bterdata["last"] < lowest:
	lowest = bterdata["last"]

f = open('/path/to/coinbasevalue.txt','w')
f.write('Average Dogecoin value' + lowest + '\n')
milliondoge = float(lowest)*1000000
dogeinusd = milliondoge * float(coinbasedata['subtotal']['amount'])
f.write('value of 1m DOGE in USD' + str(dogeinusd) + '\n')
f.close()

f = open('/path/to/dogecoinvalue.txt','w')
f.write('Current value of DOGE in BTC:' +' Cryptsy: ' + cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"] + " -- Volume: " + cryptsydata["return"]["markets"]["DOGE"]["volume"] + " Today's trend: " + cryptsytrend + " \n")
f.write('Current value of DOGE in BTC:' +' Vircurex: '+ vircurexdata["value"] + " -- Volume: " + vircurexvoldata["value"] + " Today's trend: " + vircurextrend + " \n")
f.write('Current value of DOGE in BTC:' +' COINS-E: ' + coinsedata["bid"] + " -- Volume: " + coinsedata["total_ask_q"] + " Today's trend: " + coinsetrend + " \n")
f.write('Current value of DOGE in BTC:' +' BTER: ' + bterdata["last"] + " -- Volume: " + str(bterdata["vol_doge"]) + " Today's trend: " + btertrend + " \n")
f.write('Current approx. value of 1M DOGE in USD: ' + str(dogeinusd) + " #dogecoin \n")
f.write('Direct message me with the name of one of the exchanges I check to get more current information \n')
f.close()

f = open('/path/to/cryptsyvalue.txt','w')
f.write('Current value of DOGE in BTC:' +' Cryptsy: ' + cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"] + " -- Volume: " + cryptsydata["return"]["markets"]["DOGE"]["volume"] + " Today's trend: " + cryptsytrend)
f.close()

f = open('/path/to/vircurexvalue.txt','w')
f.write('Current value of DOGE in BTC:' +' Vircurex: '+ vircurexdata["value"] + " -- Volume: " + vircurexvoldata["value"] + " Today's trend: " + vircurextrend)
f.close()

f = open('/path/to/coinsevalue.txt','w')
f.write('Current value of DOGE in BTC:' +' COINS-E: ' + coinsedata["bid"] + " -- Volume: " + coinsedata["total_ask_q"] + " Today's trend: " + coinsetrend)
f.close()

f = open('/path/to/btervalue.txt','w')
f.write('Current value of DOGE in BTC:' +' BTER: ' + bterdata["last"] + " -- Volume: " + str(bterdata["vol_doge"]) + " Today's trend: " + btertrend)
f.close()
