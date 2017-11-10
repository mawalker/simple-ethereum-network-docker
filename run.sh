#!/bin/bash
###############################################################################
#
# This Scipt builds the Dockerfile for 'RighteousCoder/openJDK-8'
#
# It logs the start and stop time and stdout & stderr into log.txt
#
###############################################################################

# Define a timestamp function
timestamp() {
  date +"%T"
}

#####################################################

log="log.txt"

timestamp | tee -a $log # print timestamp to screen & log

#docker build -t righteouscoder/geth-simple-network . 2>&1 | tee -a $log

timestamp | tee -a $log # print timestamp to screen & log

