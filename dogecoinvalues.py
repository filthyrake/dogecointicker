# Dogecoin Ticker Twitter Bot
# Written by Damen Knight
# Copyright 2014
#

from __future__ import print_function
import json
import urllib2
import os
import ctypes
import datetime
import time
libc = ctypes.cdll.LoadLibrary('libc.so.6')
res_init = libc.__res_init

res_init()

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

f2 = open('/path/to/cryptsytrend.txt','r')
f2v = f2.readline()
f2.close()

f3 = open('/path/to/vircurextrend.txt','r')
f3v = f3.readline()
f3.close()

f4 = open('/path/to/coinsetrend.txt','r')
f4v = f4.readline()
f4.close()

f5 = open('/path/to/btertrend.txt','r')
f5v = f5.readline()
f5.close()

if f2v < cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]:
	cryptsytrend = "up"
if f2v == cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]:
	cryptsytrend = "stable"
if f2v > cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]:
	cryptsytrend = "down"

if f3v < vircurexdata["value"]:
	vircurextrend = "up"
if f3v == vircurexdata["value"]:
	vircurextrend = "stable"
if f3v > vircurexdata["value"]:
	vircurextrend = "down"

if f4v < coinsedata["bid"]:
	coinsetrend = "up"
if f4v == coinsedata["bid"]:
	coinsetrend = "stable"
if f4v > coinsedata["bid"]:
	coinsetrend = "down"

if f5v < bterdata["last"]:
	btertrend = "up"
if f5v == bterdata["last"]:
	btertrend = "stable"
if f5v > bterdata["last"]:
	btertrend = "down"

lowest = cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"]
lowexchange = "cryptsy"
if vircurexdata["value"] < lowest:
        lowest = vircurexdata["value"]
        lowexchange = "vircurex"
if coinsedata["bid"] < lowest:
        lowest = coinsedata["bid"]
        lowexchange = "coins-e"
if bterdata["last"] < lowest:
        lowest = bterdata["last"]
        lowexchange = "bter"


f = open('/path/to/coinbasevalue.txt','w')
f.write('Average Dogecoin value' + lowest + '\n')
milliondoge = float(lowest)*1000000
dogeinusd = milliondoge * float(coinbasedata['subtotal']['amount'])
f.write('value of 1m DOGE in USD' + str(dogeinusd) + '\n')
f.close()

now = datetime.datetime.now().strftime("%m/%d/%y %H:%M")

f = open('/path/to/dogecoinvalue.txt','w')
f.write('Current value of DOGE in BTC:' +' Cryptsy: ' + cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"] + " -- Volume: " + cryptsydata["return"]["markets"]["DOGE"]["volume"] + " Today's trend: " + cryptsytrend + " at " + now + "\n")
f.write('Current value of DOGE in BTC:' +' Vircurex: '+ vircurexdata["value"] + " -- Volume: " + vircurexvoldata["value"] + " Today's trend: " + vircurextrend + " at " + now + " \n")
f.write('Current value of DOGE in BTC:' +' COINS-E: ' + coinsedata["bid"] + " -- Volume: " + coinsedata["total_ask_q"] + " Today's trend: " + coinsetrend + " at " + now + " \n")
f.write('Current value of DOGE in BTC:' +' BTER: ' + bterdata["last"] + " -- Volume: " + str(bterdata["vol_doge"]) + " Today's trend: " + btertrend + " at " + now + " \n")
f.write('Current approx. value of 1M DOGE in USD: $' + str(dogeinusd) + " values from " + lowexchange + " + coinbase" + " at " + now + " #dogecoin \n")
f.write('Direct message me with the name of one of the exchanges I check to get more current information \n')
f.close()

f = open('/path/to/cryptsyvalue.txt','w')
f.write('Current value of DOGE in BTC:' +' Cryptsy: ' + cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"] + " -- Volume: " + cryptsydata["return"]["markets"]["DOGE"]["volume"] + " Today's trend: " + cryptsytrend + " at " + now )
f.close()

f = open('/path/to/vircurexvalue.txt','w')
f.write('Current value of DOGE in BTC:' +' Vircurex: '+ vircurexdata["value"] + " -- Volume: " + vircurexvoldata["value"] + " Today's trend: " + vircurextrend + " at " + now )
f.close()

f = open('/path/to/coinsevalue.txt','w')
f.write('Current value of DOGE in BTC:' +' COINS-E: ' + coinsedata["bid"] + " -- Volume: " + coinsedata["total_ask_q"] + " Today's trend: " + coinsetrend + " at " + now)
f.close()

f = open('/path/to/btervalue.txt','w')
f.write('Current value of DOGE in BTC:' +' BTER: ' + bterdata["last"] + " -- Volume: " + str(bterdata["vol_doge"]) + " Today's trend: " + btertrend + " at " + now)
f.close()
