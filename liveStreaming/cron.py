import xml.etree.ElementTree as ET
import urllib
import urllib2


url = 'http://128.2.213.102:8282/stat'

def getStreamConnNum(root, streamName):
    root = root.find('server').find('application').find('live')
    for stream in root.findall('stream'):
        sName = stream.find('name').text
        if sName == streamName:
            node = stream.find('nclients')
            return node.text
    return 0

def getAllConnNum(root):
    root = root.find('server').find('application').find('live')
    node = root.find('nclients')
    return node.text

def getOutBandw(root):
    node = root.find('bw_out')
    return node.text

def getXmlString():
    req = urllib2.Request(url)
    rsp = urllib2.urlopen(req)
    retCode = rsp.getcode()
    content = rsp.read()
    return content

def getStreamInfo(root):
    infoArray = []
    root = root.find('server').find('application').find('live')
    for stream in root.findall('stream'):
        sName = stream.find('name').text
        sBandIn = stream.find('bw_in').text
        sBandOut = stream.find('bw_out').text
        infoTuple = (sName, sBandIn, sBandOut)
        infoArray.append(infoTuple)
    return infoArray

if __name__ == "__main__":
    #tree = ET.parse('test.xml')
    #root = tree.getroot()
    xmlString = getXmlString()
    root = ET.fromstring(xmlString)
    infoArray = getStreamInfo(root)
    for tuple in infoArray:
        print tuple[0], tuple[1], tuple[2]
