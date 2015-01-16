import subprocess
import os
from pymongo import MongoClient

# Check whether user has specified config.py .
# If so, get all values in config.py.
mongo_userinfo = os.getenv("MONGO_USERINFO", None)
print mongo_userinfo
if mongo_userinfo:
    with open(mongo_userinfo, "r") as rf:
        lines = rf.readlines()
        import_context = "\n".join(lines)
        exec(import_context)

globals_var = globals()

# Get necessary variable by globals(). If not, get it from environments or use default if there is none.
admin_user = globals_var["MONGO_ADMIN"] if "MONGO_ADMIN" in globals_var else os.getenv("MONGO_ADMIN", "admin")
admin_pwd = globals_var["MONGO_ADMIN_PWD"] if "MONGO_ADMIN_PWD" in globals_var else os.getenv("MONGO_ADMIN_PWD" ,"adminpwd")
mongo_port = globals_var["MONGO_PORT"] if "MONGO_PORT" in globals_var else int(os.getenv("MONGO_PORT", 27017))
mongo_logpath = globals_var["MONGO_LOGPATH"] if "MONGO_LOGPATH" in globals_var else os.getenv("MONGO_LOGPATH", None)
mongo_dbpath = globals_var["MONGO_DBPATH"] if "MONGO_DBPATH" in globals_var else os.getenv("MONGO_DBPATH", "/data/db")
mongo_users = globals_var["MONGO_USERS"] if "MONGO_USERS" in globals_var else eval(os.getenv("MONGO_USERS", '[{"user":"mongo", "pwd":"mongo", "roles":[{"role":"readWrite", "db":"test"}]}]'))
mongo_config = globals_var["MONGO_CONFIG"] if "MONGO_CONFIG" in globals_var else os.getenv("MONGO_CONFIG", "/var/mongodb.conf")

# Start mongod
cmd = "mongod --port {port} --dbpath {dbpath} --logpath /tmp/tmp.log --fork --smallfiles"
msg = "[MongoDB] Running mongod at port {port}, dbpath {dbpath} in order to add users.\n"
print cmd.format(port = mongo_port, dbpath = mongo_dbpath)
subprocess.call(cmd.format(port = mongo_port,
                           dbpath = mongo_dbpath), shell = True)
print msg.format(port=mongo_port, dbpath=mongo_dbpath)

# Initialize a MongoClient.
client = MongoClient(port = mongo_port)
admin_db = client.admin

# Add user administrator.
print "[MongoDB] Add user administrator.\n"
admin_db.add_user(admin_user, admin_pwd, roles=[{"role":"userAdminAnyDatabase", "db":"admin"}])

# Authenticate with admin account.
admin_db.authenticate(admin_user, admin_pwd)

# Add users.
print "[MongoDB] Add users.\n"
print mongo_users
for user in mongo_users:
    if user["roles"][0] == "roots":
        print "root!"
        db = client["admin"]
        db.add_user(user["user"], user["pwd"], roles = ["root"])
    else:
        db = client[user["roles"][0]["db"]]
        db.add_user(user["user"], user["pwd"], roles=user["roles"])

# Shut down mongod
print "[MongoDB] Setup complete. Shutting down mongod.\n"
shutdown_msg = subprocess.check_output("ps aux | grep mongod | grep -v grep | awk '{print $2}' | xargs kill | echo '[MongoDB] Sucessfully shut down mongod.'", shell = True)
print shutdown_msg
print "[MongoDB] Remove temp log files.\n"
subprocess.call("rm /tmp/tmp.log", shell = True)

# Start mongod if the user want it running in daemon mode.
if mongo_logpath:
    cmd = "echo 'mongod --auth --config {config} --port {port} --dbpath {dbpath} --logpath {logpath}' > /home/scripts/mongod_start.sh"
    subprocess.call(cmd.format(port = mongo_port, 
                               dbpath = mongo_dbpath, 
                               logpath = mongo_logpath,
                               config = mongo_config), shell = True)
    subprocess.call("echo 'export MONGO_PORT={mongo_port}' >> ~/.bashrc".format(mongo_port = mongo_port), shell = True)
    subprocess.call("echo 'export MONGO_DBPATH={mongo_dbpath}' >> ~/.bashrc".format(mongo_dbpath= mongo_dbpath), shell = True)
    print "[MongoDB] Running mongod at port {port} with dbpath {dbpath}, logpath {logpath}.\n".format(port = mongo_port,
                                                                                                      dbpath = mongo_dbpath,
                                                                                                      logpath = mongo_logpath)
else:
    cmd = "echo 'mongod --auth --config {config} --port {port} --dbpath {dbpath}' > /home/scripts/mongod_start.sh"
    subprocess.call(cmd.format(port = mongo_port, 
                               dbpath = mongo_dbpath,
                               config = mongo_config), shell = True)
    subprocess.call("echo 'export MONGO_PORT={mongo_port}' >> ~/.bashrc".format(mongo_port = mongo_port), shell = True)
    subprocess.call("echo 'export MONGO_DBPATH={mongo_dbpath}' >> ~/.bashrc".format(mongo_dbpath= mongo_dbpath), shell = True)
    print "[MongoDB] Running mongod at port {port} with dbpath {dbpath}.\n".format(port = mongo_port,
                                                                                   dbpath = mongo_dbpath)
