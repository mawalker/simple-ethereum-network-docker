# Project to build a simple Ethereum network within a single Docker container.

### @Author Michael A. Walker

This git repository stores multiple docker image repositories in subfolders.

### How to build the images from the git repository:
#### Only required if you want to build locally and not download the images from Docker Hub.

``` ./build.sh ```

### How to start an instance of the images in this repo:

``` ./run.sh ```

This will start up a new instance of the docker image for you and log you into it.

Then, start the geth clients via:

``` ./workspace/start-geth.sh ```

Then, run the following script to connect the two geth clients into a small private network.

``` ./workspace/networkGethClients.py ```

Then, run the following script to wait until the private test network is ready (Miner is mining blocks)

``` ./workspace/waitUntilReady.sh ```

After a few moments(Depending on your system's hardware), the geth clients will be started and the miner will finished with its startup process.

You can check the current block number of the miner via the following command since the miner client runs its administration port on port 11000. Whereas, the other client runs its administation port on port 9000. 

Query the miner client about the current block it has and the number of clients connected to it via:

``` ./workspace/pycurlGetBlockNumber.py 127.0.0.1 11000 ``` 

Query the other client about its current block and the number of clients connected to it via:

``` ./workspace/pycurlGetBlockNumber.py 127.0.0.1 9000 ``` 

### Running the project Test 

Example projects will demonstrate something via the ./workspace/testProject.py file. Run it to see the output and then examine its code to see what it is demonstrating.

```./workspace/testProject.py ```

