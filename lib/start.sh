#!/bin/bash

python2.7 /root/scripts/start.py
ps aux | grep mongod | grep -v grep | awk '{print $2}' | xargs kill
source ~/.bashrc

echo $MONGO_DAEMONIZE $MONGO_PORT $MONGO_DBPATH $MONGO_LOGPATH
if [[ "$MONGO_DAEMONIZE" == "False" ]]; then
	echo "False"
	mongod --auth --port $MONGO_PORT --dbpath $MONGO_DBPATH --smallfiles
else
	echo "True"
	mongod --auth --port $MONGO_PORT --logpath /share/db.log --dbpath $MONGO_DBPATH --fork --smallfiles
	cat /share/db.log
fi