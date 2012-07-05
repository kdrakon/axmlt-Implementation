#!/usr/bin/python

import xml.dom.minidom
import binascii


'----------------------------------------------------------------------------------------------------------------------'
def labelNodes(nl, level, nodeCount):
    
    nc = nodeCount
    
    for n in nl:    
        if n.nodeName[0:1] != "#":
            identity = n.nodeName + str(level) + str(nc)
            hashed_identity =  binascii.crc32(identity) & 0xffffffff
            hashed_identity = hex(hashed_identity)[2:]
            n.setAttribute("id", str(hashed_identity))            
            
            if len(n.childNodes) > 0:
                nc = labelNodes(n.childNodes, level + 1, nc)
            
            nc+=1
            
    return nc
    
    
    
'----------------------------------------------------------------------------------------------------------------------'


fh = open('nutrition.xml', 'r+')
xmldom = xml.dom.minidom.parse(fh)
fh.close()

nl = xmldom.childNodes

labelNodes(nl, 0, 0)

fh = open('nutrition.xml', 'w')
fh.write(xmldom.toxml())
fh.close()
