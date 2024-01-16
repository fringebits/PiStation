# PiFarm
Scraps of code from initial setup of Raspberry Pi, Visual Studio Code, and Python

*** WARNING *** this repo is a work in progress *** WARNING ***

Crontab entries:

Update.py - runs hourly
0 * * * * PiFarm/Update.py >/dev/null 2>&1

Monitor.py -- runs every 10m
*/10 * * * * * PiFarm/Monitor.py >/dev/null 2>&1


