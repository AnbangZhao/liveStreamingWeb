import xml.etree.ElementTree as ET
import urllib
import urllib2
from config import CONFIG


url = 'http://127.0.0.1:8282/stat'
reportUrl = 'http://127.0.0.1:8000/noviewer'

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

def sendReq(url, params):
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    rsp = urllib2.urlopen(req)
    retCode = rsp.getcode()
    content = rsp.read()
    return (retCode, content)

def reportNoViewer(streamName):
    url = reportUrl
    params = {}
    params[CONFIG['appname']] = 'liveStreaming'
    params[CONFIG['stream']] = streamName
    sendReq(url, params)


def report(infoArray):
    for tuple in infoArray:
        name = tuple[0]
        bwin = int(tuple[1])
        bwout = int(tuple[2])
        if bwin != 0 and bwout == 0:
            reportNoViewer(name)

if __name__ == "__main__":
    #tree = ET.parse('test.xml')
    #root = tree.getroot()
    xmlString = getXmlString()
    root = ET.fromstring(xmlString)
    infoArray = getStreamInfo(root)
    report(infoArray)

    for tuple in infoArray:
        print tuple[0], tuple[1], tuple[2]
