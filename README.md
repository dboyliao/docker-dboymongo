[dboyliao/docker-dboymongo](https://github.com/dboyliao/docker-dboymongo)
======

# Docker Image for Fast Users Setup

### This docker image config all users, including user administrator, through userinfo.py

See ```lib/userinfo_sample.py``` for all available settings.

### Basic Usage

```
docker run -it -p 27017:27017 dboyliao/docker-dboymongo
```

**It may takes a while to setup MongoDB**

- Then, type following command in your terminal shell

	- <strong> Linux </strong>: ```mongo localhost:27017```

	- <strong> OS X (boot2docker) </strong>: ```mongo the.ip.for.boot2docker:27017``` (This one is BUGGY!)
	
**There is some issues about the filesystem for docker on OS X. I haven't found a solution for running mongod in docker on OS X. Sorry....**

- You now should be able to connect to mongo and the users are setted according to default values. See ```lib/userinfo_sample.py``` for all default values.

### Passing User Information

Also, you can easily pass user information through environment variables.

For example, run:
```
docker run -it -p 27017:27017 -e "MONGO_ADMIN=qmal" -e "MONGO_ADMIN_PWD=qmalpwd" dboyliao/docker-dboymongo
``` 

Then you should be able to login MongoDB as a user adminstrator with username="qmal" and password="qmalpwd".

### Passing Outer userinfo.py Into Docker
Suppose you put your ```userinfo.py``` under ```/home/dboy```.

There is a empty folder ```/share``` in this docker image to share outer files into it.

Type:
```
docker run -it -p 27017:27017 -v /home/dboy:/share -e "MONGO_CONFIG=/share/userinfo.py" dboyliao/docker-dboymongo
```

Then the mongod is set according to ```userinfo.py```.


### Enjoy!

======