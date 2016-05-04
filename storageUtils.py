# File Storage Utility
# Version 0.2 patch 0
# Ryan Sharp - 4/27/16


from os.path import isfile,join
from xml.etree.ElementTree import parse,ElementTree,Element

def hasFile(file, path):
	print('Looking for file: %s in path: %s... ' % (file,path),end='')
	if isfile(join(path,file)):
		print(' FOUND.\n')
		return True
	else:
		print(' NOT FOUND.\n')
		return False



if __name__ == '__main__':

        from tempfile import gettempdir	

        print('\n\n******Storage Utilities V0.1.00******\n')
        Tree = getFile('LXIdevices.xml',gettempdir())
        print(Tree)
