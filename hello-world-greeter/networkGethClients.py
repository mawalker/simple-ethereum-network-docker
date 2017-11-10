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
    results = rpcCommand(ip=ip,port=port,method="eth_sendTransaction",params=[{'from':account, 'to':toAddress, 'data': dataString, 'gas': gas}])
    if verbose == 'True':
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

    contract = "6060604052341561000f57600080fd5b60405161050c38038061050c83398101604052808051820191905050336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508060019080519060200190610081929190610088565b505061012d565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100c957805160ff19168380011785556100f7565b828001600101855582156100f7579182015b828111156100f65782518255916020019190600101906100db565b5b5090506101049190610108565b5090565b61012a91905b8082111561012657600081600090555060010161010e565b5090565b90565b6103d08061013c6000396000f300606060405260043610610062576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806341c0e1b51461006757806342cbb15c1461007c578063a4136862146100a5578063cfae321714610102575b600080fd5b341561007257600080fd5b61007a610190565b005b341561008757600080fd5b61008f610221565b6040518082815260200191505060405180910390f35b34156100b057600080fd5b610100600480803590602001908201803590602001908080601f01602080910402602001604051908101604052809392919081815260200183838082843782019150505050505091905050610229565b005b341561010d57600080fd5b610115610243565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561015557808201518184015260208101905061013a565b50505050905090810190601f1680156101825780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561021f576000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b565b600043905090565b806001908051906020019061023f9291906102eb565b5050565b61024b61036b565b60018054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156102e15780601f106102b6576101008083540402835291602001916102e1565b820191906000526020600020905b8154815290600101906020018083116102c457829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061032c57805160ff191683800117855561035a565b8280016001018555821561035a579182015b8281111561035957825182559160200191906001019061033e565b5b509050610367919061037f565b5090565b602060405190810160405280600081525090565b6103a191905b8082111561039d576000816000905550600101610385565b5090565b905600a165627a7a72305820e7812a25721d9dac54df990f9c3a8c3dc30748387348e6b1e8ce1cec451aed130029"

    greetHash = "cfae3217";
    setGreetingHash = "a4136862"

    # get enode info from non-miner client
    results = getEnodeInfo("127.0.0.1", "9000", verbose='True')

    # convert enode into fully appropriate string version
    results = results.split("@")[0] + "@127.0.0.1:8001"

    # add the peer to the miner's client statically
    results2 = addPeer("127.0.0.1", "11000", results)
