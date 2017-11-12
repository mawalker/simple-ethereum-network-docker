#!/usr/bin/python3

##############################################################################
#
# Sample program to interact with ethereum RPC "2.0" with python.
#
#    Uses pycurl to HTTP POST query and returns json data.
#
# @Author   Michael A. Walker
# @Date     2017-08-06
#
##############################################################################

import pprint
import pycurl
import json
import sys
from io import BytesIO
import time

def rpcCommand(method,params=[],ip='localhost',port='9012',id=1,jsonrpc="2.0",verbose=False,exceptions=False):
    """ Method to abstract away 'curl' usage to interact with RPC of geth clients.
        Will throw error if attempting to connect to a client that doesn't exist.
    """
    # the <ip:port> to connect to
    ipPort = str(ip) + ":" + str(port)
    # buffer to capture output
    buffer = BytesIO()
    # start building curl command to process
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.URL, ipPort)
        c.setopt(pycurl.HTTPHEADER, ['Accept:application/json'])
        c.setopt(pycurl.WRITEFUNCTION, buffer.write)
        data2 = {"jsonrpc":str(jsonrpc),"method": str(method),"params":params,"id":str(id)}
        data = json.dumps(data2)
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        if verbose:
            c.setopt(pycurl.VERBOSE, 1)
        #perform pycurl
        c.perform()

        # check response code (HTTP codes)
        if (c.getinfo(pycurl.RESPONSE_CODE) != 200):
            if exceptions:
                raise Exception('rpc_communication_error', 'return_code_not_200')
            return {'error':'rpc_comm_error','desc':'return_code_not_200','error_num':None}
        #close pycurl object
        c.close()
    except pycurl.error as e:
        c.close()
        errno, message = e.args
        if exceptions:
            raise Exception('rpc_communication_error', 'Error No: ' + errno + ", message: " + message)
        return {'error':'rpc_comm_error','desc':message,'error_num':errno}


    # decode result
    results = str(buffer.getvalue().decode('iso-8859-1'))
    if verbose:
        print (results)

    # convert result to json object for parsing
    data = json.loads(results)
    # return appropriate result
    if 'result' in data.keys():
        return data["result"]
    else:
        if 'error' in data.keys():
            if exceptions:
                raise Exception('rpc_communication_error', data)
            return data
        else:
            if exceptions:
                raise Exception('rpc_communication_error', "Unknown Error: possible method/parameter(s) were wrong and/or networking issue.")
            return {"error":"Unknown Error: possible method/parameter(s) were wrong and/or networking issue."}


##############################################################################
# Helper methods to simplify blockchain interactions.
##############################################################################

def getPeerCount(ip,port,verbose=False):
    """ Get number of peers connected to target client. """
    results = rpcCommand(ip=ip,port=port,method="net_peerCount",params=[])
    if verbose == 'True':
        print ("number of peers connected to client at: " + ip + ":" + port + " is: " + results)
    return results

def getAccounts(ip,port,verbose=False):
    """ Get list of accounts on target geth client """
    results = rpcCommand(ip=ip,port=port,method="eth_accounts",params=[])
    if verbose == 'True':
        print ("Accounts: " + result)
    return results

def getBalance(ip,port,account=None,blockParameter="latest", verbose=False):
    """ Get balance of an account. Defaults to first account in client.
          blockParameter defaults to "latest", valid options are:
            String "earliest" for the earliest/genesis block
            String "latest" - for the latest mined block
            String "pending" - for the pending state/transactions
    """
    if blockParameter not in ['earliest', 'latest', 'pending']:
        return "blockParameter was not a valid option: 'earliest', 'latest', 'pending'."
    if account == None:
        if verbose == 'True':
            print ("No account given, querying first account on cliennt.")
        account = rpcCommand(ip=ip,port=port,method='eth_accounts')[0]
        if verbose == 'True':
            print ("   Account Number: " + account)
    results = rpcCommand(ip=ip,port=port,method="eth_getBalance",params=[account,blockParameter])
    if verbose == 'True':
        print( "Account:" +account + ", latest balance: " + results)
    return results

def addPeer(ip,port,enode,verbose=False):
    """ Add a peer to this client."""
    results = rpcCommand(ip=ip,port=port,method="admin_addPeer",params=[enode])
    if verbose == 'True':
        print (results)
    return results

def getEnodeInfo(ip,port,verbose=False):
    """ Get the node info of this client. """
    results = rpcCommand(ip=ip,port=port,method="admin_nodeInfo",params=[])
    if verbose == 'True':
        print ("Enode: " + results['enode'])
    return results['enode']

def deployContract(ip,port,gas = "0x200000", contractBytecode="", account=None,verbose=False):
    if account == None:
        account = getAccounts(ip,port)[0]
        if verbose == 'True':
            print ("No acocunt provided, first acocunt on this client will be used: " + account)
    # Could add future check to see if account balance is suffient enough.
    # balance = getBalance(ip,port,results1[0])
    # balanceNeeded = .... calculation of contract size + gas offering, etc.
    # print ( "balance is not enough, ohly has: " + balance + " needs: " + balanceNeeded)
    results = rpcCommand(ip=ip,port=port,method="eth_sendTransaction",params=[{'from':account, 'data': contractBytecode,'gas': gas}])
    if verbose == 'True':
        print ("Transaction results:" + results)
    # return receipt.
    return results


def getAddressOfTransaction(ip,port,transactionReceipt,account=None,verbose='False'):
    if account == None:
        account = getAccounts(ip,port)[0]
        if verbose == 'True':
            print ("No acocunt provided, first acocunt on this client will be used: " + account)
    results = rpcCommand("eth_getTransactionReceipt", params=[transactionReceipt], ip=ip, port=port)
    if verbose == 'True':
        print ("TransactionReceipt:")
        pprint.pprint(results)
    return results


def callContractMethod(ip,port,toAddress,dataString,gas="0x200000",account=None,verbose=False):
    if account == None:
        account = getAccounts(ip,port)[0]
        if verbose == 'True':
            print ("No acocunt provided, first acocunt on this client will be used: " + account)
    # Could add future check to see if account balance is suffient enough.
    # balance = getBalance(ip,port,results1[0])
    # balanceNeeded = .... calculation of contract size + gas offering, etc.
    # print ( "balance is not enough, ohly has: " + balance + " needs: " + balanceNeeded)
    params=[{'from':account, 'to':toAddress, 'data': dataString, 'gas': gas}]
    if verbose == 'True':
        print ("Call Contract Method Transaction Parameters:")
        pprint.pprint(params)
    results = rpcCommand(ip=ip,port=port,method="eth_sendTransaction",params=params)
    if verbose == 'True':
        if isinstance(results,dict):
            print ("Transaction results:")
            pprint.pprint(results)
        else:
            print ("Transaction results:" + results)
    return results

def getFilterChanges(ip,port,filterID,verbose=False):
    """ Get filter changes based on filter ID """
    results = rpcCommand(ip=ip,port=port,method="eth_getFilterChanges",params=[filterID])
    if verbose == 'True':
        print ("Filtered Events for FilterID <"+str(filterID)+">:")
        pprint.pprint(results)
    return results

def getBlockNumber(ip,port,verbose='False'):
    """ Get current block number. """
    results = rpcCommand(ip=ip,port=port,method="eth_blockNumber",params=[])
    if verbose == 'True':
        print ("Current block number is: " + results)
    return results

def getTransactionByHash(ip,port,hash,verbose='False'):
    """ Returns the information about a transaction requested by transaction hash. """
    results = rpcCommand(ip=ip,port=port,method='eth_getTransactionByHash',params=[hash])
    if verbose == 'True':
        print ("Transaction by hash:")
        pprint.pprint(results)
    return results

def makeNewFilter(ip,port,fromBlock="0x1",verbose='False'):
    # returned filter ID
    newFilterID = rpcCommand("eth_newFilter", params=[{'fromBlock':fromBlock}], ip=ip, port=port)
    if verbose == 'True':
        print ("Transaction by hash:" + newFilterID)
    return newFilterID

def ethCall(ip,port,toAddress,dataString,gas="0x200000",account=None,verbose=False):
    """ Executes a new message call immediately without creating a transaction on the block chain. """
    if account == None:
        account = getAccounts(ip,port)[0]
        if verbose == 'True':
            print ("No acocunt provided, first acocunt on this client will be used: " + account)
    # Could add future check to see if account balance is suffient enough.
    # balance = getBalance(ip,port,results1[0])
    # balanceNeeded = .... calculation of contract size + gas offering, etc.
    # print ( "balance is not enough, ohly has: " + balance + " needs: " + balanceNeeded)
    params=[{'from':account, 'to':toAddress, 'data': dataString, 'gas': gas}, "latest"]
    if verbose == 'True':
        print ("Call Contract Method Transaction Parameters:")
        pprint.pprint(params)
    results = rpcCommand(ip=ip,port=port,method="eth_call",params=params)
    if verbose == 'True':
        if isinstance(results,dict):
            print ("Transaction results:")
            pprint.pprint(results)
        else:
            print ("Transaction results:" + results)
    return results

##############################################################################
# Experimental methods, not guarenteed to work!!!!!!
##############################################################################



def callMethodLocally(ip,port):
    address = listAccounts(ip,port)
    print (address)
    zeroInt32= "1".rjust(64,'0')
    print (zeroInt32)
    paramValues = {'to':address[0], 'gas':'0x20000', 'data':"0xcfae3217"+zeroInt32}
#    paramValues = {'to':address[0], 'gas':'0x20000', 'data':"0x23b87507" +zeroInt32+zeroInt32+zeroInt32+zeroInt32}
    results = rpcCommand(ip=ip,port=port,method='eth_call',params=[paramValues,"latest"])
    print (results)

def callMethod(ip,port):
    address = listAccounts(ip,port)
    print (address)
    paramValues = {'from':address[0],'to':address[0], 'gas':'0x20000', 'data':'0xf8a8fd6d'}
    results = rpcCommand(ip=ip,port=port,method='eth_sendTransaction',params=[paramValues])
    print (results)

def callMethod2(ip,port):
    address = listAccounts(ip,port)
    print (address)
    zeroInt32= "".rjust(64,'0')
    print (zeroInt32)
    paramValues = {'from':address[0],'to':address[0], 'gas':'0x20000', 'data':"0x23b87507" +zeroInt32+zeroInt32+zeroInt32+zeroInt32}
    results = rpcCommand(ip=ip,port=port,method='eth_sendTransaction',params=[paramValues])
    print (results)


def getHash(ip,port):
    paramValues = {"test()"}
    results = rpcCommand( ip=ip, port=port, method='eth_call', params=["test()"] )
    print (results)


##############################################################################
# 'main' entrypoint of script
##############################################################################

if __name__ == '__main__':

    #################################################
    # Contract name
    #################################################
    # SimpleStorage

    #################################################
    # Contract
    #################################################
    # pragma solidity ^0.4.8;
    # contract SimpleStorage {
    #     uint storedData;
    #     function set(uint x) public {
    #         storedData = x;
    #     }
    #     function get() public constant returns (uint retVal) {
    #         return storedData;
    #     }
    # }
    #################################################

    #################################################
    # Meta-Data about contract
    #################################################
    # {"compiler":{"version":"0.4.18+commit.9cf6e910"},"language":"Solidity","output":{"abi":[{"constant":false,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}],"devdoc":{"methods":{}},"userdoc":{"methods":{}}},"settings":{"compilationTarget":{"browser/ballot.sol":"SimpleStorage"},"libraries":{},"optimizer":{"enabled":false,"runs":200},"remappings":[]},"sources":{"browser/ballot.sol":{"keccak256":"0xbfa1a74f0356c93ad686e709e09bbdf374a18cf24cc32bdf0bb352914c092a2c","urls":["bzzr://7159d4c5db004937669eae9635a772fd69657c123a4ab4113fbb3ba324300794"]}},"version":1}

    #################################################
    # Interface ABI
    #################################################
    # [{"constant":false,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]

    #################################################
    # Web3Deploy JS
    #################################################
    # var browser_ballot_sol_simplestorageContract = web3.eth.contract([{"constant":false,"inputs":[{"name":"x","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get","outputs":[{"name":"retVal","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]);
    # var browser_ballot_sol_simplestorage = browser_ballot_sol_simplestorageContract.new(
    #    {
    #       from: web3.eth.accounts[0],
    #       data: '0x6060604052341561000f57600080fd5b60d38061001d6000396000f3006060604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806360fe47b114604e5780636d4ce63c14606e575b600080fd5b3415605857600080fd5b606c60048080359060200190919050506094565b005b3415607857600080fd5b607e609e565b6040518082815260200191505060405180910390f35b8060008190555050565b600080549050905600a165627a7a723058206569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad29390029', 
    #       gas: '4700000'
    #    }, function (e, contract)
    #    {
    #       console.log(e, contract);
    #       if (typeof contract.address !== 'undefined')
    #       {
    #          console.log('Contract mined! address: ' + contract.address + ' transactionHash: ' + contract.transactionHash);
    #       }
    #    }
    # )

    #################################################
    # Contract & RuntimeBytecode
    #################################################
    SimpleStorageContract = "0x6060604052341561000f57600080fd5b60d38061001d6000396000f3006060604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806360fe47b114604e5780636d4ce63c14606e575b600080fd5b3415605857600080fd5b606c60048080359060200190919050506094565b005b3415607857600080fd5b607e609e565b6040518082815260200191505060405180910390f35b8060008190555050565b600080549050905600a165627a7a723058206569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad29390029"
    SimpleStorageRuntimeBytecode = "0x6060604052600436106049576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806360fe47b114604e5780636d4ce63c14606e575b600080fd5b3415605857600080fd5b606c60048080359060200190919050506094565b005b3415607857600080fd5b607e609e565b6040518082815260200191505060405180910390f35b8060008190555050565b600080549050905600a165627a7a723058206569c46c09feaa724076844fe37ec8fd0c9086ae2e72f1c0e93ed5852bad29390029"

    #################################################
    # SimpleStorage Function Hashses
    #################################################
    # "6d4ce63c": "get()",
    # "60fe47b1": "set(uint256)"
    #################################################
    SimpleStorageGetHash = "0x6d4ce63c"
    SimpleStorageSetHash = "0x60fe47b1"

    # input to set value to '2'
    SimpleStorageSet2 = "0x60fe47b10000000000000000000000000000000000000000000000000000000000000002"

    #################################################
    # Logic to submit/operate/filter a contract
    #################################################

    # ipAddr = sys.argv[1]
    # portAddr = sys.argv[2]

    # Statically set for this example, would normally use Command Line Interface (CLI) args above
    ipAddr = "127.0.0.1"
    portAddr = "9000"

    # Time to sleep after submitting a transaction to allow the block to be mined (public test network is 5~7+ minutes)
    sleepTime = 30 # seconds

    # Make a new filter (locally). Note: Filter doesn't yet have any info about contract so similar to "*" search.
#    newFilterID = makeNewFilter(ip=ipAddr,port=portAddr,fromBlock="0x0",verbose='False')
#    print ("New Filter ID: " + str(newFilterID))

    # Submit the contract as a transaction.
    contractTransactionReceipt = deployContract (
                                        ip = ipAddr,
                                        port = portAddr,
                                        contractBytecode = SimpleStorageContract,
                                        verbose='False'
                                      )

    print ("Smart Contract Submission TransactionReceipt: ")
    pprint.pprint(contractTransactionReceipt)

    # Sleep for some time to allow mining of transaction's block to finish.
    print ("Sleeping for " + str(sleepTime) + " seconds to allow for mining of transaction." + "\n")
    time.sleep(sleepTime)

    # get the address of the contract, after its transaction has been mined into a complete block.
    contractAddress = getAddressOfTransaction (
                                               ip = ipAddr,
                                               port = portAddr,
                                               transactionReceipt = contractTransactionReceipt,
                                               verbose = 'False'
                                             ) ['contractAddress']

    print ("Contract Address: " + contractAddress)


    # Call 'get()' in the smart contract.
    methodLocalCallResuls = ethCall (
                                             ip = ipAddr,
                                             port = portAddr,
                                             toAddress = contractAddress,
                                             dataString = SimpleStorageGetHash,
                                             gas = "0x200000",
                                             account = None,
                                             verbose = 'True'
                                           )

    print ("Method Local Call Results:")
    pprint.pprint(methodLocalCallResuls)


    # Call 'get()' in the smart contract.
    MethodCallTransactionReceipt = callContractMethod (
                                              ip = ipAddr,
                                              port = portAddr,
                                              toAddress = contractAddress,
                                              dataString = SimpleStorageSet2,
                                              gas = "0x200000",
                                              account = None,
                                              verbose = 'True'
                                            )

    # Sleep for some time to allow mining of transaction's block to finish.
    print ("Sleeping for " + str(sleepTime) + " seconds to allow for mining of transaction." + "\n")
    time.sleep(sleepTime)

    # get the block number, after its transaction has been mined into a complete block.
    # NOTE: this isn't the ideal way to check this in a production system, since this call would error
    # if transaction has not yet been mined, (let alone many other possible scenarios)
    methodCallTransaction = getAddressOfTransaction (
                                                 ip = ipAddr,
                                                 port = portAddr,
                                                 transactionReceipt = MethodCallTransactionReceipt,
                                                 verbose = 'True'
                                               )
    methodCallBlockNumber = methodCallTransaction['blockNumber']

    print ("MethodCall Transaction BlockNumber: " + methodCallBlockNumber + "\n")

    # Check the Filter for any changes.
#    changeResults = getFilterChanges(ip=ipAddr,port=portAddr,filterID=newFilterID,verbose="True")
#    pprint.pprint(changeResults)

