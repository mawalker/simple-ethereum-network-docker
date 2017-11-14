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
FROM ubuntu:16.04

##############################################################################
# Define the MAINTAINER
##############################################################################
MAINTAINER Michael A. Walker "michael.a.walker.1@vanderbilt.edu"

##############################################################################
# Update apt-get info (quietly)
##############################################################################
RUN apt-get update -qq

##############################################################################
# This software provides an abstraction of the used apt repositories.
# It allows you to easily manage your distribution and independent software
# vendor software sources. --- This package contains the common files for
# software-properties like the D-Bus backend.
# Reference(s):
# http://packages.ubuntu.com/trusty/software-properties-common
# https://packages.debian.org/sid/admin/software-properties-common
#
# 'might' not need this, unsure, in for safety for now.
#
##############################################################################
RUN apt-get install -y --no-install-recommends software-properties-common

##############################################################################
# Install some commons software to help with scripts, etc.
# These are all likely to be very small and helpful
##############################################################################
RUN apt-get install -y zip unzip less wget curl dtach nano vim tmux

RUN mkdir -p /workspace/ethereum/
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
COPY waitUntilReady.sh /workspace/waitUntilReady.sh
