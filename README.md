# Project to build a simple Ethereum network within a single Docker container.

### @Author Michael A. Walker

### How to build this image from the git repository:

``` ./build.sh ```

### How to start an instance of this image:

``` ./run.sh ```

This will start up a new instance of the docker image for you and log you into it.

Then, start the geth clients via:

``` cd /workspace/start-geth.sh ```

After a few moments, the geth clients will be started and the miner will finished with its startup process.

You can check the current block number of the miner via the following command since the miner client runs its administration port on port 11000. Whereas, the other client runs its administation port on port 9000. 

``` ./workspace/pycurlGetBlockNumber.py 127.0.0.1 11000 ``` 


