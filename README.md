dogecointicker
==============

Written by Damen Knight

Copyright 2014


Installation/usage instructions

setup the following cron jobs (with changes made as appropriate for your paths and the location of the scripts):


*/5 * * * * /usr/bin/python /path/to/dogecoinvalues.py

*/60 * * * * /usr/bin/python /path/to/dogecointicker.py /path/to/dogecoinvalue.txt

00 00 * * * /usr/bin/python /path/to/resetvalues.py

* * * * * /usr/bin/python /path/to/dmlistener.py


The first cron job: Every 5 minutes get current dogecoin values

The second cron job: Every hour, tweet

The third cron job: Every night at midnight, reset the base value for the day for each exchange

The fourth cron job: Every minute, check for Direct Messages and reply if appropriate


Modify dogecointicker.py and dmlistener.py to include your twitter API credentials for tweeting.
Modify all appropriate python files and replace /path/to/ with the correct paths to wherever you put the files
Modify the crontab listings and replace /path/to/ with the correct paths for wherever you put the files
