# XML Object Handler
# Version 0.2 Patch 2
# Ryan Sharp - 5/2/16

from xml.etree.ElementTree import Element as _Element, ElementTree as _ElementTree, dump as _dump, fromstring as _fromstring, parse as _parse
from http.client import HTTPConnection, CannotSendRequest
import storageUtils as SU
from os import chdir

def getLocalTree(file, path, RootName='Devices'):

    print('\ngetLocalTree Called.\n')
    
    print('Getting XML File: %s from path: %s... ' % (file,path))
    if SU.hasFile(file, path):
        print('Parsing file... ',end='')
        chdir(path)
        Tree = _parse(file)
        # Root = Tree.getroot()
        print('DONE.\n')
    else:
        print('Building XML File... ',end='')
        Tree = _ElementTree()
        Root = _Element(RootName)
        Tree._setroot(Root)
        Tree.write(join(path,file))
        print('DONE.\n')
    return Tree

def getWebElem(host):

    print('\ngetWebElem Called.\n') 

    Root = None

    print('Creating HTTP Connection to %s... ' % (host),end='')
    c = HTTPConnection(host)
    print('SUCCESS.')
    # print('\n',c,'\n')
    print('Trying to send request to host... ',end='')
    try:
        c.request("GET", "/home.cgi")
        print('SENT.')
    except TimeoutError:
        print('CONNECTION TIMEOUT.')
    except OSError as inst:
        print(inst)
    except CannotSendRequest:
        print('CANNOT SEND.')
    except:
        print('Unkown Error Occurred While Trying to Request Data.')
    else:
        print('Getting Reply... ')
        r = c.getresponse()
        print('Decoding... ')
        xml = r.read().decode("UTF-8")
        print('Closing HTTP Connection...')
        c.close()
        print('Parsing webpage...')
        Root = _fromstring(xml)
    print('\ngetWebElem Done.')
    return Root

def getWebXML(host):

    print('\ngetWebXML Called.\n') 

    Root = None

    print('Creating HTTP Connection to %s... ' % (host),end='')
    c = HTTPConnection(host)
    print('SUCCESS.')
    # print('\n',c,'\n')
    print('Trying to send request to host... ',end='')
    try:
        c.request("GET", "/home.cgi")
        print('SENT.')
    except TimeoutError:
        print('CONNECTION TIMEOUT.')
    except OSError as inst:
        print(inst)
    except CannotSendRequest:
        print('CANNOT SEND.')
    except:
        print('Unkown Error Occurred While Trying to Request Data.')
    else:
        print('Getting Reply... ')
        r = c.getresponse()
        print('Decoding... ')
        xml = r.read().decode("UTF-8")
        print('Closing HTTP Connection...')
        c.close()
        print('Parsing webpage...')
        Root = _fromstring(xml)
    print('\ngetWebElem Done.')
    return Root

def filterTags(Elem, tags, NewRootName=None):
    '''Filter Element and returning only those tags and text that match the list 'tags'''
    print('\nfilterTags Called.\n')
    
    outRoot = None
    if len(list(Elem)) > 0:
        if NewRootName == None:
            NewRootName = Elem.tag[Elem.tag.index('}') + 1:]
        # _dump(Elem)
        print('Generating empty output element with root tag: %s.' % (NewRootName))
        outRoot = _Element(NewRootName)              #Create empty output root element
        # _dump(outRoot)
        for t in tags:                              #For a tag in 'tags'
            print('\nFiltering element tags for %s...' % (t),end='')
            for e in Elem.iter():                     #For all elements and children in 'Elem'
                eTag = e.tag[e.tag.index('}') + 1:]              #Make a new string from the tag without the garbage
                # print('\nLooking in %s... ' % (eTag), end='')
                if eTag == t:                       #If the new string matches the tag
                    print('FOUND.')
                    if t == 'SerialNumber':             #If the tag is the serial number...
                        outRoot.set(t,e.text)               #make it the root tag of outRoot, with text as attrib
                    print('Copying Tag name and Text to outRoot... ',end='')
                    ex = _Element(eTag)                 #Make a new subelement with garbage-collected tag
                    ex.text = e.text                    #Copy the element text from input to output
                    outRoot.append(ex)                  #Append new element to the Device root element
                    print(ex.tag,ex.text)
                    break                               #Don't keep searching the input root if element is found
    else:
        print('Passed Empty Element, Nothing to Filter.')
    print('\nfilterTags Done')
    return outRoot              #Return an ET Element containing all subelements in 'tags'

def buildWebTree(hostlist,tags,RootName='Devices'):
    print('\nbuildWebTree Called.')
    
    Tree = _ElementTree()
    Root = _Element(RootName)
    Tree._setroot(Root)

    for h in hostlist:
        print('\n********%s*******\n' % (h))
        print('Calling getWebElem...')
        xml = getWebElem(h)
        print('\nChecking for XML Data... ',end='')
        if not xml == None:
            print('GOOD.\nChecking if data is Element... ',end='')
            if not type(xml) is _Element:
                print('DATA IS: %s. Trying to parse... ' % (type(xml)))
                parsed = _fromstring(xml)
            else:
                print('DATA IS Element')
                parsed = xml
            print('Calling filterTags...')
            Device = filterTags(parsed,tags,'Device')
            print('Appending filtered elements to Root Element.')
            # _dump(Device)
            Root.append(Device)
        else:
            print('No XML Data\n')

    print('\nbuildWebTree Done.\n')
    return Tree

if __name__ == '__main__':

    print('\n********XML Utilities V0.2.00********')
    import sys

    if not len(sys.argv) > 1:
        print(
            '''\nNo arguments were passed.\nTo execute buildWebTree: python [script] build [Host IP Address]
            \nTo execute getLocalTree: python [script] local [filename]
            \nTo execute getWebElem: python [script] web [Host IP Address]
            ''')
    else:
        if sys.argv[1] == 'build':

            print('\nTESTING WEB TREEBUILDER')
            
            Tree = buildWebTree([sys.argv[2]],['SerialNumber'])
            _dump(Tree)

            
        if sys.argv[1] == 'local':

            print('\nTESTING LOCAL CONFIG FILE RETREIVE.')
            from tempfile import gettempdir

            Tree = getLocalTree(sys.argv[2],gettempdir())
            if not Tree == None:
                print('\nSuccessfully Retreived File.')
                print('\nCalling filterTags for tag "SerialNumber"...')
                newRoot = filterTags(Tree.getroot(),['SerialNumber'])

                print('\n\nData Dump:\nxmlRoot:\n')
                _dump(Tree)
                if not newRoot == None:
                    print('\nnewRoot:\n')
                    _dump(newRoot)

        if sys.argv[1] == 'web':

            xml = getWebElem(sys.argv[2])
            if not xml == None:
                print('\nSuccessfully Retreived Webpage.')
                print('\nCalling filterTags for tag "SerialNumber"...')
                newRoot = filterTags(xml,['SerialNumber'])

                print('\n\nData Dump:\nxmlRoot:\n')
                _dump(xml)
                print('\nnewRoot:\n')
                _dump(newRoot)
            
            
