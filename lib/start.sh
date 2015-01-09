#!/bin/sh

python /home/scripts/setup.py

echo "[MongoDB] Start mongod in 3 secs."
sleep 3

sh /home/scripts/mongod_start.sh