#!/bin/sh

python /home/scripts/setup.py

ehco "[MongoDB] Start mongod in 3 secs."

sh /home/scripts/mongod_start.sh