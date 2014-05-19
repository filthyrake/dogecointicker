# Dogecoin Ticker Twitter Bot
# Written by Damen Knight
# Copyright 2014

from __future__ import print_function
import json
import urllib2

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
mintpalresponse = urllib2.urlopen('https://api.mintpal.com/v1/market/stats/DOGE/BTC')
mintpaldata = json.load(mintpalresponse)

f = open('/path/to/cryptsytrend.txt','w')
f.write(cryptsydata["return"]["markets"]["DOGE"]["lasttradeprice"])
f.close()
f = open('/path/to/vircurextrend.txt','w')
f.write(vircurexdata["value"])
f.close()
f = open('/path/tocoinsetrend.txt','w')
f.write(coinsedata["bid"])
f.close()
f = open('/path/to/btertrend.txt','w')
f.write(bterdata["last"])
f.close()
f = open('/path/to/mintpaltrend.txt','w')
f.write(mintpaldata[0]["last_price"])
f.close()
