[dboyliao/docker-mongotest](https://github.com/dboyliao/docker-dboymongo)
======

# Docker Image for Fast Users Setup (Testing version -- log)

### This docker image config all users, including user administrator, through config.py

See ```config_sample.py``` for all available settings.

### Basic Usage

```
docker run -it -p 27017:27017 dboyliao/docker-dboymongo
```
- Then, type following command in your terminal shell

	- <strong> Linux </strong>: ```mongo localhost:27017```

	- <strong> OS X (boot2docker) </strong>: ```mongo the.ip.for.boot2docker:27017```

- You now should be able to connect to mongo and the users are setted according to default values. See ```config_sample.py``` for all default values.

### Passing Outer config.py Into Docker
Suppose you put your ```config.py``` under ```/Users/DboyLiao/Dockerfiles/docker-dboymongo```.

There is a empty folder ```/share``` in this docker image to share outer files into it.

Type:
```
docker run -it -p 27017:27017 -v /Users/DboyLiao/Dockerfiles/docker-dboymongo:/share -e "MONGO_CONFIG=/share/config.py" dboyliao/docker-dboymongo
```

Then the mongod is set according to ```config.py```.

### Enjoy!

======

# Issues to Be Solved.

- Can not pass evironment variable (except for "MONGO_CONFIG") through -e flage.