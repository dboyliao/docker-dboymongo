FROM c3h3/openblas

# ENV for pyenv.
ENV HOME /root
ENV PYENVPATH $HOME/.pyenv
ENV PATH $PYENVPATH/shims:$PYENVPATH/bin:$PATH

# Install MongoDB.
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen' | tee /etc/apt/sources.list.d/mongodb.list
RUN apt-get update && apt-get install -y mongodb-org && chown -R root:root /var/lib/mongodb

# Make a empty share directory for outer-files to be shared. Setup default mongodb dbpath.
RUN mkdir -p /data/db /share 

# Prettify ls
RUN echo "alias ls=\"ls --color='auto' -p\"" >> /root/.bashrc

# Install git.
RUN apt-get update && apt-get install -y git-core

# Install ps related binary cmd.
RUN apt-get install -y apt-utils
RUN apt-get install -y --reinstall procps build-essential

# Install necessary C-compiler and install python.
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
RUN echo 'eval "$(pyenv init -)"' >> /root/.bashrc
RUN pyenv install 2.7.8 && pyenv global 2.7.8 && pip install pymongo

# Install nano.
RUN apt-get install -y nano

# Prettify nano.
RUN git clone https://github.com/dboyliao/nanorc_files /root/nanorc && touch /root/.nanorc
RUN ls /root/nanorc | grep -v man-html | grep -v README.md | awk '{print "include /root/nanorc/" $1}' >> /root/.nanorc

# Adding .py and .js files
RUN mkdir /root/scripts

ADD lib/* /root/scripts/
ADD mongod.conf /var/mongod.conf

EXPOSE 27017

CMD python2.7 /root/scripts/start.py && sh /root/mongod.sh
