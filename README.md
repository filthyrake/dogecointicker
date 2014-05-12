dogecointicker
==============
Written by Damen Knight
Copyright 2014

Installation/usage instructions
setup the following cron jobs (with changes made as appropriate for your paths and the location of the scripts):

*/5 * * * * /usr/bin/python dogecoinvalues.py
*/60 * * * * /usr/bin/python dogecointicker.py dogecoinvalue.txt
00 00 * * * /usr/bin/python resetvalues.py

The first cron job: Every 5 minutes get current dogecoin values
The second cron job: Every hour, tweet
The third cron job: Every night at midnight, reset the base value for the day for each exchange


Modify dogecointicker.py to include your twitter API credentials for tweeting.
