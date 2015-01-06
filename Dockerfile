FROM debian

# Add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN groupadd -r mongodb && useradd -r -g mongodb mongodb

# Installing curl and git.
RUN apt-get update && apt-get install -y curl git-core && rm -rf /var/lib/apt/lists/*

# Grab gosu for easy step-down from root
RUN gpg --keyserver pgp.mit.edu --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture)" \
	&& curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture).asc" \
	&& gpg --verify /usr/local/bin/gosu.asc \
	&& rm /usr/local/bin/gosu.asc \
	&& chmod +x /usr/local/bin/gosu

ENV MONGO_RELEASE_FINGERPRINT DFFA3DCF326E302C4787673A01C4E7FAAAB2461C
RUN gpg --keyserver pgp.mit.edu --recv-keys $MONGO_RELEASE_FINGERPRINT

ENV MONGO_VERSION 2.6.6

RUN curl -SL "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-$MONGO_VERSION.tgz" -o mongo.tgz \
	&& curl -SL "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-$MONGO_VERSION.tgz.sig" -o mongo.tgz.sig \
	&& gpg --verify mongo.tgz.sig \
	&& tar -xvf mongo.tgz -C /usr/local --strip-components=1 \
	&& rm mongo.tgz*

# Make a empty share directory for outer-files to be shared.
RUN mkdir /share

# Prettify ls
RUN echo "alias ls=\"ls --color='auto' -p\"" >> /root/.bashrc

# Install ps related binary cmd.
RUN apt-get install -y apt-utils
RUN apt-get install -y --reinstall procps build-essential

# Install necessary C-compiler and install python.
RUN apt-get install -y python-pip && pip install pymongo

# Install nano.
RUN apt-get install -y nano

# Prettify nano.
RUN git clone https://github.com/dboyliao/nanorc_files /root/nanorc && touch /root/.nanorc
RUN ls /root/nanorc | grep -v man-html | grep -v README.md | awk '{print "include /root/nanorc/" $1}' >> /root/.nanorc

# Adding .py and .js files
RUN mkdir /root/scripts

ADD lib/* /root/scripts/

EXPOSE 27017

WORKDIR /root/scripts

RUN chmod +x start.sh

CMD ./start.sh
