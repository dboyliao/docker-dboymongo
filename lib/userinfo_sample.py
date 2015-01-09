MONGO_ADMIN = "admin" # Username for user administrator.
MONGO_ADMIN_PWD = "adminpwd" # Password for user administrator.
MONGO_PORT = 27017 # Port for mongod to run at.
MONGO_DBPATH = '/data/db' # Data files path for mongod.
MONGO_LOGPATH = '/share/mongodb.log'
# Users to be added.
MONGO_USERS = [{"user":"mongo", "pwd":"mongo", "roles":[{"role":"readWrite", "db":"test"}]}]
MONGO_CONFIG = '/var/mongodb.conf'