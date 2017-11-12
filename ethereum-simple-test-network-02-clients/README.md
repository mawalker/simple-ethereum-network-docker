# Ethereum Simple private test network with 02 clients

This project is publicly available at: https://hub.docker.com/r/righteouscoder/ethereum-simple-test-network-02-clients/

------

## How to build this project locally

### Skip this step if you want to just download the publicly available image.

Then run [ ./build.sh ] in this directory.

--------

## How to use this project

Run [ ./run.sh ] in this directory. This will launch an instance of the custom docker image of this project.

Now that you are in the custom docker image, run these commands to 

1) change directory to where the scripts are

2) start the geth clients 

3) network them together 

4) wait until the network is ready and then use it.

```
cd /workspace/
./start-geth.sh 
./networkGethClients.py 
./waitUntilReady.sh
```
