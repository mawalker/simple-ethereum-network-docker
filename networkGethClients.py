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

    # get enode info from non-miner client
    results = getEnodeInfo("127.0.0.1", "9000", verbose='True')

    # convert enode into fully appropriate string version
    results = results.split("@")[0] + "@127.0.0.1:8001"

    # add the peer to the miner's client statically
    results2 = addPeer("127.0.0.1", "11000", results)
