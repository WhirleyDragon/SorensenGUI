# Network Device Tracker Class
# Version 0.1 patch 1
# Ryan Sharp - 5/2/16

import vxiUtils as VXI
import cliUtils as CLI


class NetTracker:
    """Creates a NetTracker Object to track multiple networked devices."""

    
    def __init__(self):

        print('NetTracker Instantiation Called.\nCreating new instance.')
        print('init Called...\nCreating default attributes.')
        
        self.pingPackets = 1
        self.pingTime = 10
        self.allIP = []
        self.reachableIP = []
        self._found = []

        self.Search()

        print('\nDone.')

    def Search(self):

        print('Search Called...\nSearching for VXI-11 Devices...')        
        self._found = VXI.Discover()
        self.Update()

    def Update(self):
        print('Testing Devices for reachability...')
        self.allIP = CLI.Ping(self._found,self.pingPackets,self.pingTime,True)
        try:
            for ip in self.allIP:
                if(self.allIP[ip]):
                    self.reachableIP.append(ip)
        except TypeError as inst:
            print(inst)

