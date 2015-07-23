FROM mongo

# Make a empty share directory for outer-files to be shared. Setup default mongodb dbpath.
# /data/db: default mongod dbpath.
# /share: an empty directory to put outer files into.
# /root/scripts: containing all helper scripts.
VOLUME ["/share", "/home/scripts"]

# Install git, ps related binary cmd and necessary C-compiler.
RUN apt-get update && apt-get install -y git-core && apt-get install -y apt-utils && apt-get install -y --reinstall procps build-essential

# Install python.
RUN apt-get install -y python-pip python-dev && pip install pymongo

# Install nano.
RUN apt-get install -y nano

# Prettify nano.
RUN git clone https://github.com/dboyliao/nanorc_files /root/nanorc && touch /root/.nanorc
RUN ls /root/nanorc | grep -v man-html | grep -v README.md | awk '{print "include /root/nanorc/" $1}' >> /root/.nanorc

# Adding .py and .js files
ADD lib/* /home/scripts/
ADD mongodb.conf /var/mongodb.conf

WORKDIR /home

CMD sh /home/scripts/start.sh
