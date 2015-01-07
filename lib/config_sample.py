MONGO_USERS = [
	{"user":"mongo", "pwd":"mongo", "roles":[{"role":"readWrite", "db":"test"}]},
	{"user":"mongo2", "pwd":"mongo2", "roles":[{"role":"readWrite", "db":"test2"}]},
	{"user":"root", "pwd":"root", "roles":["root"]}
]
MONGO_DAEMONIZE = False
MONGO_PORT = 27017
MONGO_DBPATH = '/data/db'
MONGO_LOGPATH = '/share/db.log'