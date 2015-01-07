import subprocess
import os
from pymongo import MongoClient

# Check whether user has specified config.py .
# If so, get all values in config.py.
mongo_config = os.getenv("MONGO_CONFIG", None)
if mongo_config:
    with open(mongo_config, "r") as rf:
        lines = rf.readlines()
        import_context = "\n".join(lines)
        exec(import_context)

globals_var = globals()

# Get necessary variable by globals(). If not, get it from environments or use default if there is none.
admin_user = globals_var["MONGO_ADMIN"] if "MONGO_ADMIN" in globals_var else os.getenv("MONGO_ADMIN", "admin")
admin_pwd = globals_var["MONGO_ADMIN_PWD"] if "MONGO_ADMIN_PWD" in globals_var else os.getenv("MONGO_ADMIN_PWD" ,"adminpwd")
mongo_port = globals_var["MONGO_PORT"] if "MONGO_PORT" in globals_var else int(os.getenv("MONGO_PORT", 27017))
mongo_dbpath = globals_var["MONGO_DBPATH"] if "MONGO_DBPATH" in globals_var else os.getenv("MONGO_DBPATH", "/data/db")
mongo_logpath = globals_var["MONGO_LOGPATH"] if "MONGO_LOGPATH" in globals_var else os.getenv("MONGO_LOGPATH", "/share/db.log")
mongo_users = globals_var["MONGO_USERS"] if "MONGO_USERS" in globals_var else eval(os.getenv("MONGO_USERS", '[{"user":"mongo", "pwd":"mongo", "roles":[{"role":"readWrite", "db":"test"}]}]'))

# Start mongod
cmd = "mongod --port {port} --dbpath {dbpath} --logpath {logpath} --fork --smallfiles"
msg = "[MongoDB] Running mongod at port {port}, dbpath {dbpath}, logpath {logpath}."
print cmd.format(port = mongo_port, dbpath = mongo_dbpath, logpath = mongo_logpath)
subprocess.call(cmd.format(port = mongo_port,
                           dbpath = mongo_dbpath,
                           logpath = mongo_logpath), shell = True)
print msg.format(port=mongo_port, logpath=mongo_logpath, dbpath=mongo_dbpath)

# Initialize a MongoClient.
client = MongoClient(port = mongo_port)
admin_db = client.admin

# Add user administrator.
print "[MongoDB] Add user administrator."
admin_db.add_user(admin_user, admin_pwd, roles=[{"role":"userAdminAnyDatabase", "db":"admin"}])

# Authenticate with admin account.
admin_db.authenticate(admin_user, admin_pwd)

# Add users.
print "[MongoDB] Add users"
for user in mongo_users:
    if "root" == user["roles"][0]:
        db = client["admin"]
        db.add_user(user["user"], user["pwd"], roles = ["root"])
    else:
        db = client[user["roles"][0]["db"]]
        db.add_user(user["user"], user["pwd"], roles=user["roles"])

# Shut down mongod
print "[MongDB] Setup complete. Shutting down mongod."
subprocess.call("ps aux | grep mongod | grep -v grep | awk '{print $2}' | xargs kill", shell = True)

# Start mongod if the user want it running in daemon mode.
cmd = "echo 'mongod --auth --port {port} --dbpath {dbpath} --logpath {logpath} --smallfiles' > /root/mongod.sh"
subprocess.call(cmd.format(port = mongo_port, dbpath = mongo_dbpath, logpath = mongo_logpath), shell = True)
subprocess.call("echo 'export MONGO_PORT={mongo_port}' >> ~/.bashrc".format(mongo_port = mongo_port), shell = True)
subprocess.call("echo 'export MONGO_DBPATH={mongo_dbpath}' >> ~/.bashrc".format(mongo_dbpath= mongo_dbpath), shell = True)
subprocess.call("echo 'export MONGO_LOGPATH={mongo_logpath}' >> ~/.bashrc".format(mongo_logpath = mongo_logpath), shell = True )

