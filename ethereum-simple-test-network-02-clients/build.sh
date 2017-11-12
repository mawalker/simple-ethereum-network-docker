#!/bin/bash
###############################################################################
#
# This Scipt builds the Dockerfile for
#                      'righteouscoder/ethereum-simple-test-network-02-clients'
#
# It logs the start and stop time and stdout & stderr into log.txt
#
# @Author   Michael A. Walker
# @Date     2017-11-10
#
###############################################################################

# Define a timestamp function
timestamp() {
  date +"%T"
}

#####################################################

log="log.txt"

timestamp | tee -a $log # print timestamp to screen & log

docker build -t righteouscoder/ethereum-simple-test-network-02-clients . 2>&1 | tee -a $log

timestamp | tee -a $log # print timestamp to screen & log

