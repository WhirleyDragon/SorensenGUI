# Sorensen Power Panel
# Version: 0.06 patch 2
# Ryan Sharp - 5/2/16

import NetTracker as NT
import xmlUtils as XML

tags = ['SerialNumber','MACAddress','Hostname','UserDescription','Manufacturer','Model','FirmwareRevision']
	
# NewDevices = buildTree(tags)
# ET.dump(NewDevices)
# print('\n')

# import TestFinder as Finder
# from tempfile import gettempdir

# OldDevices = Finder.get('LXIDevices.xml',gettempdir())
# ET.dump(OldDevices)

# #combine new and old, flag if new not in old

# def combineXML(aTree, bTree):
	# NDF = False 	#New Device Flag

if __name__ == '__main__':

        from tempfile import gettempdir

        print('\n\n******Sorensen Power Supply Backend V0.03.00******\n')
	
        tracker = NT.NetTracker()
        print(tracker.allIP)

        
        
        if not tracker.reachableIP == None:
                WebTree = XML.buildWebTree(tracker.reachableIP,tags)

                print('\n\n******Dumping Results******\n')
                XML._dump(WebTree)
        else:
                print('\nDone.')


        LocTree = XML.getLocalTree('LXIDevices.xml',gettempdir())

        XML._dump(LocTree)

##        MTree = XML.MergeTrees(WebTree,LocTree)     #Make merge and check if new devices



##      local xml tree: <Device Selected="bool" SerialNumber="string">
