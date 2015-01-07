#!/bin/bash

python2.7 /root/scripts/start.py
ps aux | grep mongod | grep -v grep | awk '{print $2}' | xargs kill
source ~/.bashrc

echo $MONGO_PORT $MONGO_DBPATH $MONGO_LOGPATH
mongod --auth --port $MONGO_PORT --dbpath $MONGO_DBPATH --logpath $MONGO_LOGPATH --smallfiles