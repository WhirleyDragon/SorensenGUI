# VXI-11 RPC Discovery Module
# Version 0.2 Patch 0
# Ryan Sharp - 4/27/16


from xdrlib import Packer
from random import random
from time import time
from select import select
import socket


CALL = 0
PORTMAP = 100000
GETPORT = 3
AUTH_NULL = 0
VXI11_CORE = 395183
TCP = 6


def _rpcPacket():			#Build RPC portmap call
        
    data = Packer()
    data.pack_uint(int(random() * 0xffffffff))       # Transaction Identifier (xid)
    data.pack_enum(CALL)                                    # Message Type
    data.pack_uint(2)                                       # RPC version
    data.pack_enum(PORTMAP)                                 # Program 
    data.pack_uint(2)                                       # Program Version
    data.pack_enum(GETPORT)                                 # Process
    data.pack_enum(AUTH_NULL)                               # Credentials
    data.pack_uint(0)                                       # Credentials length
    data.pack_enum(AUTH_NULL)                               # Verifier 
    data.pack_uint(0)                                       # Verifier Length
    data.pack_enum(VXI11_CORE)                              # Called Program
    data.pack_uint(1)                                       # Program Version
    data.pack_enum(TCP)                                     # Program Protocol
    data.pack_uint(0)                                       # Port
    
    return data.get_buffer()

def readSockAddr(mySock, timeout):  # TODO: write in timeout feature so that replies will be recorded until no activity for x time
    
    readcycle = time() + timeout
    msg = []
    while(readcycle > time()):
        if len(checkSock([mySock])[0]) > 0:
            msg.append(mySock.recvfrom(64)[1])  #tuple of string Addr and int Port
            print('Response from: %s' % ((msg[-1])[0]))
            readcycle = time() + timeout
    return msg


def checkSock(mySock_list):
    from select import select
    
    canread, canwrite, haserr = select(mySock_list, mySock_list, [], 1)
    checklist = [canread, canwrite, haserr]
    return checklist


def writeSock(mySock, data, dest):
    
    print('Checking Writeability... ',end='')
    if len(checkSock([mySock])[1]) > 0:
        print('GOOD')
        print('Broadcasting Port Mapper... ',end='')
        bites = mySock.sendto(data, dest)
        print('%d BYTES SENT.' % (bites))
    else:                       # Implement error checking here
        bites = 0
        print('NOT AVAILABLE')
    return bites


def Discover():
    
    print('Creating Discovery Socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    writeSock(s, _rpcPacket(), ('<broadcast>', 111))
    replyList = []
    print('Reading Replies and Filtering for IP Addresses...','\n')
    for t in readSockAddr(s, 0.1):        #for tuple in list of tuples, timeout is 3 seconds
        replyList.append(t[0])          #append entry at [0] to list (discard ports)
    print('\nClosing Socket.')
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    print('\nDone.')
    return replyList

if __name__ == '__main__':
    import sys

    print('\n****************************')
    print('\nRunning Discovery Script...\n')

    Discover()
