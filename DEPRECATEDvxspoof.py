#vxspoof

import socket
import select
import xdrlib
import random
import time
import xml.etree.ElementTree as ET
import http.client as HC


CALL = 0
PORTMAP = 100000
GETPORT = 3
AUTH_NULL = 0
VXI11_CORE = 395183
TCP = 6

tags = ['SerialNumber','MACAddress','Hostname','UserDescription','Manufacturer','Model','FirmwareRevision']

NDL = {'IP ADDR':['Serial Number', 'MAC ADDR', 'Host Name', 'User Description', 'Manufacturer', 'Model', 'Firmware Version',{}]}

ActivDict = {}


def rpcPacket():			#Build RPC portmap call
	data = xdrlib.Packer()
	data.pack_uint(int(random.random() * 0xffffffff))		# Transaction Identifier (xid)
	data.pack_enum(CALL)									# Message Type
	data.pack_uint(2)										# RPC version
	data.pack_enum(PORTMAP)									# Program 
	data.pack_uint(2)										# Program Version
	data.pack_enum(GETPORT)									# Process
	data.pack_enum(AUTH_NULL)								# Credentials
	data.pack_uint(0)										# Credentials length
	data.pack_enum(AUTH_NULL)								# Verifier 
	data.pack_uint(0)										# Verifier Length
	data.pack_enum(VXI11_CORE)								# Called Program
	data.pack_uint(1)										# Program Version
	data.pack_enum(TCP)										# Program Protocol
	data.pack_uint(0)										# Port
	return data.get_buffer()
	
def checkSock(mySock_list):
	canread, canwrite, haserr = select.select(mySock_list, mySock_list, [], 1)
	checklist = [canread, canwrite, haserr]
	return checklist

def writeSock(mySock, data, dest):
	#print('Checking Writeability... ',end="")
	if len(checkSock([mySock])[1]) > 0:
		bytes = mySock.sendto(data, dest)
		check = 0
	else:
		bytes = 0
		check = 1
	w = xdrlib.Packer()
	w.pack_int(check)
	w.pack_int(bytes)
	return w.get_buffer()
	
def readSockAddr(mySock, timeout):
	readcycle = time.time() + timeout
	msg = []
	while(readcycle > time.time()):
		if len(checkSock([mySock])[0]) > 0:
			msg.append(mySock.recvfrom(64)[1])
	#print(msg)
	return msg

def Discover():
	print('Creating Discovery Socket...')
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	print('Broadcasting Port Mapper...')
	writeSock(s, rpcPacket(), ('<broadcast>', 111))
	replyList = []
	print('Reading Replies and Filtering for IP Addresses...','\n')
	for t in readSockAddr(s, 3):   		#for tuple in list of tuples, timeout is 3 seconds
		replyList.append(t[0])			#append entry at [0] to list (discard ports)
		print('Response From: ',t[0])
	print('\n','Closing Socket','\n')
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	return replyList
	
def getXML(host):
	c = HC.HTTPConnection(host)
	try:
		c.request("GET", "/home.cgi")
	except HC.HTTPException as inst:
		print('HTTP Request Error: ', inst)
	except OSError as inst:
		print(inst)
	except:
		print('Unkown Error Occurred While Trying to Request Data')
	else:
		r = c.getresponse()
		xml = r.read().decode("UTF-8")
		c.close()
		return xml

def parseXMLTags(xml, tags):	#Parse XML String 'xml', returning only those tags and text that match the list 'tags'
	from xml.etree.ElementTree import Element, fromstring
	inRoot = ET.fromstring(xml)		#Parse xml string
	#dump(inRoot)
	outRoot = ET.Element('Device')				#Create empty output root element
	#dump(outRoot)
	for t in tags:								#For a tag in 'tags'
		for e in inRoot.iter():						#For all elements and children in 'inRoot'
			#print(e)
			garbend = e.tag.index('}') + 1		#Measure the garbage in the tag string
			eTag = e.tag[garbend:]				#Make a new string from the tag without the garbage
			#print(eTag,'\n')
			if eTag == t:						#If the new string matches the tag
				if t == 'SerialNumber':				#If the tag is the serial number...
					outRoot.set(t,e.text)				#make it the root tag of outRoot, with text as attrib
				ex = Element(eTag)					#Make a new subelement with garbage-collected tag
				ex.text = e.text					#Copy the element text from input to output
				outRoot.append(ex)					#Append new element to the Device root element
				print(ex.tag,ex.text)
				break								#Don't keep searching the input root if element is found
	print('\n')
	return outRoot				#Return an ET Element containing all subelements in 'tags'
	
'''def buildNetDevList():			#
	DiscoList = Discover()		#
	for d in DiscoList:
		idlist = []
		print('\n')
		print(d, ': ')
		data = getXML(d)					#get xml data
		#print(data, '\n')
		idlist = parseXMLTags(data, tags)	#parse headers into idlist
		print(idlist, '\n')
		idlist.append(ActivDict)
		NDL[d] = idlist						#build NDL[d] = idlist
	return NDL'''

def buildTree(tags):
	from xml.etree.ElementTree import Element,ElementTree,dump
	Tree = ET.ElementTree()
	Root = ET.Element('Devices')
	Tree._setroot(Root)

	for d in Discover():
		print('********',d,'*******','\n')
		xml = getXML(d)
		if not xml == None:
			Device = parseXMLTags(xml, tags)
			ET.dump(Device)
			print('\n')
			Root.append(Device)
		else:
			print('No XML Data\n')
	return Tree
	
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
	
DiscoList = Discover()
# print('disco output: ')
# print(DiscoList)

from subprocess import run
pingstring = "ping -n 1 -w 10 "

Rdict = {}
if(len(DiscoList)>0):	
	for d in DiscoList:
		Rdict[d] = run(pingstring + d,shell = True).returncode
	print(Rdict)
else:
	print('No Devices.')

