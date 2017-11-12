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
# copy specific files for this example
##############################################################################
COPY testProject.py /workspace/testProject.py
COPY waitUntilReady.sh /workspace/waitUntilReady.sh
COPY fullTest.sh /fullTest.sh

