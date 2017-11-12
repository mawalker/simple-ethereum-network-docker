#!/bin/bash

###############################################################################
#
# This Scipt runs an instance of 'righteouscoder/ethereum-greeter-example'
#
# @Author  Michael A. Walker
# @Date    2017-11-10
#
###############################################################################

echo "\n\n  Waiting for Network Miner to start mining.  \n\n"

results=$(./pycurlGetBlockNumber.py 127.0.0.1 9000 | grep "Current block number is:" | awk {'print $5'})

while [ "$results" = "0x0" ]; do
   sleep 2
   results=$(./pycurlGetBlockNumber.py 127.0.0.1 9000 | grep "Current block number is:" | awk {'print $5'})
done

echo "\nMining has started. Network is ready to use.\n"
