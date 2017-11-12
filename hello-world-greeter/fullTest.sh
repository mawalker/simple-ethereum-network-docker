#!/bin/bash
###############################################################################
#
# This Scipt runs all the required sub-scripts to fully test this project
#
# @Author  Michael A. Walker
# @Date    2017-11-11
#
###############################################################################

# First, start the geth clients
# Second, network the clients statically together
# Third, wait until the network is ready
# Forth, test this project

./workspace/start-geth.sh && sleep 5 && \
./workspace/networkGethClients.py && sleep 5 && \
./workspace/waitUntilReady.sh && sleep 5 && \
./workspace/testProject.py
