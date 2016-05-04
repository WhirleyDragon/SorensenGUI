'''	PSudocoded discovery process
	Ryan Sharp
'''
'''Temporary Device List (TDL): (XML format?)
		List saved in appdata containing the lexical data: SERIAL, mac, ip add, hostname, userdesc, mfg, model, firmvers, activ
'''
''' Reduce latency by only polling for changes in status register summaries. if stat register mismatch:
	investigate which bit changed until source of change found and updated'''




''' Startup Process:
	

	build new local device list:
		Go to local\temp
		if hasfile(lxidevices.xml):
			return lxidevices.xml as devTree
		else:
			tree = ET.ElemTre()
			tree._setroot('Devices')
			tree.write(lxidevices.xml)
			return lxidevices.xml
		retreive previous device list if available:
	Compare prev and new device lists to check for matching, new, selected, devices:
	go to control menu:	
'''


import TestFinder