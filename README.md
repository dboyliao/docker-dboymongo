[dboyliao/docker-dboymongo](https://github.com/dboyliao/docker-dboymongo)
======

# Docker Image for Fast Users Setup

### This docker image config all users, including user administrator, through userinfo.py

See ```lib/userinfo_sample.py``` for all available settings.
Then you can use the environment variable ``MONGO_USERINFO`` to pass all settings.

### Basic Usage

```
docker run -it -p 27017:27017 dboyliao/smongo
```

**It may take a while to setup MongoDB**

After the setup completed, you should have a running mongod on your localhost.

- Type following command in your terminal shell to connect with mongodb.

	- Linux: ```mongo localhost:27017```

	- OS X (boot2docker): ```mongo the.ip.for.boot2docker:27017``` (This one is BUGGY!)
	
**There is some issues about the filesystem for docker on OS X. I haven't found a solution for running mongod in docker on OS X. Sorry....**

- You now should be able to connect to mongo and the users are setted according to default values. See ```lib/userinfo_sample.py``` for all default values.

### Passing Admin Information

Also, you can easily pass admin information through environment variables.

For example, run:
```
docker run -it -p 27017:27017 -e "MONGO_ADMIN=qmal" -e "MONGO_ADMIN_PWD=qmalpwd" dboyliao/smongo
``` 

Then you should be able to login MongoDB as a user adminstrator with username="qmal" and password="qmalpwd".

### Passing Outer userinfo.py Into Docker
Suppose you put your ```userinfo.py``` under ```/home/dboy```.

There is a empty folder ```/share``` in this docker image to share outer files into it.

Type:
```
docker run -it -p 27017:27017 -v /home/dboy:/share -e "MONGO_USERINFO=/share/userinfo.py" dboyliao/smongo
```

Then the mongod is set according to ```userinfo.py```.


### Enjoy!

======

Issues:
  1. Can't run on boot2docker. Need to fix the journaling issue. (without "--smallfiles" tag)