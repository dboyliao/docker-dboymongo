#!/bin/bash

python2.7 /root/scripts/start.py
source ~/.bashrc

if [[ $MONGO_DAEMONIZE == 'False' ]]; then
	mongod --auth --port $MONGO_PORT --dbpath $MONGO_DBPATH
fi