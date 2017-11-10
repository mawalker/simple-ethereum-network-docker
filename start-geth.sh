#!/bin/bash

dtach -n `mktemp -u /tmp/prosumer00001XXXXX.dtach` bash -c 'exec -a prosumer00001 geth --password /workspace/password.txt --datadir /workspace/ethereum/test_network_001_1/prosumer/00001 --networkid 15 --port 8001 --unlock 0  --verbosity 5 --rpc --rpcaddr 127.0.0.1 --rpcport  9000 --rpcapi eth,web3,admin,miner,net,db  --netrestrict 127.0.0.0/16 --nodiscover  > /workspace/ethereum/test_network_001_1/prosumer/00001/output.log 2>&1 '

dtach -n `mktemp -u /tmp/miner00001XXXXX.dtach` bash -c 'exec -a miner00001 geth --password /workspace/password.txt --datadir /workspace/ethereum/test_network_001_1/miners/00001 --networkid 15 --port 10001 --unlock 0  --verbosity 5 --rpc --rpcaddr 127.0.0.1 --rpcport  11000 --rpcapi eth,web3,admin,miner,net,db  --netrestrict 127.0.0.0/16 --nodiscover  --mine --minerthreads=1 --etherbase=0x0000000000000000000000000000000000000000 > /workspace/ethereum/test_network_001_1/miners/00001/output.log 2>&1 '
