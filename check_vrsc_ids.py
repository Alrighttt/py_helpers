#!/usr/bin/env python3
from itertools import combinations
import slickrpc
import platform
import os
import re

# define data dir
def def_data_dir():
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Windows':
        ac_dir = '%s/komodo/' % os.environ['APPDATA']
    return(ac_dir)

# fucntion to define rpc_connection
def def_credentials(chain):
    rpcport = '';
    ac_dir = def_data_dir()
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    if len(rpcport) == 0:
        if chain == 'KMD':
            rpcport = 7771
        else:
            print("rpcport not in conf file, exiting")
            print("check " + coin_config_file)
            exit(1)

    return (slickrpc.Proxy("http://%s:%s@127.0.0.1:%d" % (rpcuser, rpcpassword, int(rpcport)), timeout=10000))



#sample = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
sample = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
list_combinations = list()

#for n in range(len(sample) + 1):
#    list_combinations += list(c)

ret = list(combinations(sample, 2))

final = set()
for i in ret:
    l = ""
    for j in i:
        l += j
        final.add(l + '@')

#print(final)
#print(len(final))

rpc = def_credentials('VRSC')

unregistered = set()
for i in list(final):
    try:
        ident = rpc.getidentity(i)
    except slickrpc.exc.RpcInvalidAddressOrKey:
        unregistered.add(i)


print(list(unregistered))
print(len(list(unregistered)))
