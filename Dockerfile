FROM mongo

RUN mkdir /share

# Prettify ls
RUN echo "alias ls=\"ls --color='auto' -p\"" >> /root/.bashrc

# Install git.
RUN apt-get update && apt-get install -y git

# Install ps related binary cmd.
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

CMD sh /root/scripts/start.sh