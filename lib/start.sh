python2.7 start.py

if [[ '$MONGO_DAEMONIZE' == 'False' ]]; then
	mongod --auth --port $MONGO_PORT --dbpath $MONGO_DBPATH
fi