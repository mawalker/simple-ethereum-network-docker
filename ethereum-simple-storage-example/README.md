# Ethereum Simple Storage Example

This project is publicly available at: https://hub.docker.com/r/righteouscoder/ethereum-simple-storage-example/

------

## How to build this project locally

### Skip this step if you want to just download the publicly available image.

First, Build the geth-simple-network image by running [ ./build.sh ] in that directory.

Then run [ ./build.sh ] in this directory.

--------

## How to use this project

Then run [ ./run.sh ] in this directory. This will launch an instance of the custom docker image of this project.

Now that you are in the custom docker image, run these commands to 

1) change directory to where the scripts are

2) start the geth clients 

3) network them together 

4) wait until the network is ready and then run the testProject python file

```
cd /workspace/
./start-geth.sh 
./networkGethClients.py 
./waitUntilReady.sh && ./testProject.py
```

### Here is a sample output from the above 4th command

```
root@9d9231fed368:/workspace# ./waitUntilReady.sh && ./testProject.py 

  Waiting for Network Miner to start mining.

  Mining has started. Network is ready to use.

Smart Contract Submission TransactionReceipt: 
'0x20d5a0fbe5d28446b2d12460440278eedd5fe65c8060fd77634674bd9069efd5'
Sleeping for 60 seconds to allow for mining of transaction.

Contract Address: 0x9df96063817c1c47e3a0cc538e08fcb63c5b69fb
Method Local Call Results: 
'0x0000000000000000000000000000000000000000000000000000000000000000'
Sleeping for 60 seconds to allow for mining of transaction.

MethodCall Transaction BlockNumber: 0x39

eth_getstorageAt Params:
['0x9df96063817c1c47e3a0cc538e08fcb63c5b69fb', '0x0', 'latest']
getSimpleStorageAt results:0x0000000000000000000000000000000000000000000000000000000000000002
At Block Number: 0x51, value of contract's first variable: 0x0000000000000000000000000000000000000000000000000000000000000002
```

## The following two sets of APIs are the APIs available to you via JSON-RPC:

https://github.com/ethereum/wiki/wiki/JSON-RPC

https://github.com/ethereum/go-ethereum/wiki/Management-APIs

-------

## Here is the sample contract for this example.

```
pragma solidity ^0.4.8;
contract SimpleStorage {
    uint storedData;
    function set(uint x) public {
        storedData = x;
    }
    function get() public constant returns (uint retVal) {
        return storedData;
    }
}
```

https://ethereum.github.io/browser-solidity/#version=soljson-v0.4.18+commit.9cf6e910.js

Used remix editor to compile this contract. Below are the outputs it gives.

-------

### META DATA

{"compiler":{"version":"0.4.18+commit.9cf6e910"},"language":"Solidity","output":{"abi":[{"constant":false,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}],"devdoc":{"methods":{}},"userdoc":{"methods":{}}},"settings":{"compilationTarget":{"browser/ballot.sol":"SimpleStorage"},"libraries":{},"optimizer":{"enabled":false,"runs":200},"remappings":[]},"sources":{"browser/ballot.sol":{"keccak256":"0xbfa1a74f0356c93ad686e709e09bbdf374a18cf24cc32bdf0bb352914c092a2c","urls":["bzzr://7159d4c5db004937669eae9635a772fd69657c123a4ab4113fbb3ba324300794"]}},"version":1}

### BYTECODE

6060604052341561000f57600080fd5b60d38061001d6000396000f3006060604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806360fe47b114604e5780636d4ce63c14606e575b600080fd5b3415605857600080fd5b606c60048080359060200190919050506094565b005b3415607857600080fd5b607e609e565b6040518082815260200191505060405180910390f35b8060008190555050565b600080549050905600a165627a7a723058206569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad29390029

### Interface ABI

[{"constant":false,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]

### WEB3DEPLOY
```
var browser_ballot_sol_simplestorageContract = web3.eth.contract([{"constant":false,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]);
var browser_ballot_sol_simplestorage = browser_ballot_sol_simplestorageContract.new(
   {
     from: web3.eth.accounts[0], 
     data: '0x6060604052341561000f57600080fd5b60d38061001d6000396000f3006060604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806360fe47b114604e5780636d4ce63c14606e575b600080fd5b3415605857600080fd5b606c60048080359060200190919050506094565b005b3415607857600080fd5b607e609e565b6040518082815260200191505060405180910390f35b8060008190555050565b600080549050905600a165627a7a723058206569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad29390029', 
     gas: '4700000'
   }, function (e, contract){
    console.log(e, contract);
    if (typeof contract.address !== 'undefined') {
         console.log('Contract mined! address: ' + contract.address + ' transactionHash: ' + contract.transactionHash);
    }
 })
```

### METADATAHASH
 
6569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad2939
 
### SWARMLOCATION
 
bzzr://6569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad2939
 
### FUNCTIONHASHES

```
{
   "6d4ce63c": "get()",
   "60fe47b1": "set(uint256)"
}
```

### GASESTIMATES

```
{
    "Creation": "88 + 42200\n",
    "External": {
        "get()": 416,
        "set(uint256)": 20178
    },
    "Internal": {}
}
```

### RUNTIME BYTECODE

6060604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806360fe47b114604e5780636d4ce63c14606e575b600080fd5b3415605857600080fd5b606c60048080359060200190919050506094565b005b3415607857600080fd5b607e609e565b6040518082815260200191505060405180910390f35b8060008190555050565b600080549050905600a165627a7a723058206569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad29390029

