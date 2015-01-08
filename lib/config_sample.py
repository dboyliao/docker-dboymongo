MONGO_ADMIN = "admin" # Username for user administrator.
MONGO_ADMIN_PWD = "adminpwd" # Password for user administrator.
MONGO_PORT = 27017 # Port for mongod to run at.
MONGO_DBPATH = '/data/db' # Data files path for mongod.
# Users to be added.
MONGO_USERS = [
	{"user":"mongo", "pwd":"mongo", "roles":[{"role":"readWrite", "db":"test"}]},
	{"user":"mongo2", "pwd":"mongo2", "roles":[{"role":"readWrite", "db":"test2"}]},
	{"user":"root", "pwd":"root", "roles":["root"]}
]