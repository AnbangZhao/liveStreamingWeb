import xml.etree.ElementTree as ET
import urllib
import urllib2
from config import CONFIG
import os
from time import sleep


url = 'http://127.0.0.1:8282/stat'
reportUrl = 'http://127.0.0.1:8000/noviewer'
reportErrorUrl = 'http://127.0.0.1:8000/error'
heartbeatUrl = "https://p2p-meta-server.appspot.com/heartbeat"
rootStatusUrl = "https://p2p-meta-server.appspot.com/rootstatus"
CLOUDLET_NAME = 'cloudletName'
INTERVAL = 15

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

def getTreeName(appname, streamName):
    treename = appname + "/" + streamName
    return treename

def getIp():
    userHome = os.getenv("HOME")
    filepath = userHome + '/ip'
    ipFile = open(filepath, 'r')
    ipList = []
    for line in ipFile:
        ipList.append(line.rstrip())
    return ipList

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


def heartbeat(streamName, localip):
    url = heartbeatUrl
    treeName = getTreeName('liveStreaming', streamName)
    params = dict(treename=treeName)
    params[CLOUDLET_NAME] = localip
    print 'heartbeat params:', params
    sendReq(url, params)


def getRootStatus(streamName):
    url = rootStatusUrl 
    treeName = getTreeName('liveStreaming', streamName)
    params = dict(treename=treeName)   
    retTuple = sendReq(url, params)
    return retTuple[1]


def reportError(streamName):
    status = getRootStatus(streamName)
    print 'root status', status
    url = reportErrorUrl
    params = {}
    params[CONFIG['appname']] = 'liveStreaming'
    params[CONFIG['stream']] = streamName
    params[CONFIG['rootStatus']] = status
    sendReq(url, params)
    # if this node is root and is not a new node. exit
    # if this node is not root, check if root is good
    # if root is good, reschedule
    # if root is not good, exit

def report(infoArray, localip):
    for tuple in infoArray:
        name = tuple[0]
        bwin = int(tuple[1])
        bwout = int(tuple[2])
        if bwin == 0:
            reportError(name)
        elif bwout == 0:
            reportNoViewer(name)
        if bwin != 0:
            heartbeat(name, localip)

if __name__ == "__main__":
    #tree = ET.parse('test.xml')
    #root = tree.getroot()
    while True:
        ipList = getIp()
        localip = ipList[0]
        xmlString = getXmlString()
        root = ET.fromstring(xmlString)
        infoArray = getStreamInfo(root)
        report(infoArray, localip)

        for tuple in infoArray:
            print tuple[0], tuple[1], tuple[2]

        sleep(INTERVAL)
