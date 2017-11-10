##############################################################################
###
### Dockerfile to build a self-contained Ethereum network.
###
###    Network will contain 1 miner and N clients.
###       N=1 for now, might change to be build-time argument.
###
##############################################################################

##############################################################################
# Define the parent image
##############################################################################
FROM righteouscoder/geth-simple-network

##############################################################################
# Define the MAINTAINER
##############################################################################
MAINTAINER Michael A. Walker "michael.a.walker.1@vanderbilt.edu"

##############################################################################
# Update apt-get info (quietly)
##############################################################################
RUN apt-get update -qq

RUN mkdir -p /workspace/greeter/

RUN mkdir -p /workspace/geth/ && cd /workspace/geth/
RUN apt-get install -y python-pycurl

RUN curl -o geth.tar.gz https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.7.2-1db4ecdc.tar.gz
RUN tar -zxvf geth.tar.gz -C /workspace/geth/ --strip-components=1

RUN ls -la /workspace/ && ls -la /workspace/geth/
RUN cp /workspace/geth/geth /usr/bin/geth

ADD directory.tar.gz /workspace/ethereum/

COPY start-geth.sh /workspace/start-geth.sh

RUN echo "password" > /workspace/password.txt

copy pycurlGetBlockNumber.py /workspace/pycurlGetBlockNumber.py

copy networkGethClients.py /workspace/networkGethClients.py
