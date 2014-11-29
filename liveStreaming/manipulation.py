from liveStreaming.httpService import *
import os

# def createTree(appname, streamName, streamCapacity):
#     treeName = getTreeName(appname, streamName)
#     createTreeUrl = "https://p2p-meta-server.appspot.com/createtree"
#     values = dict(treename=treeName, consume=streamCapacity)
#     data = urllib.urlencode(values)
#     req = urllib2.Request(createTreeUrl, data)
#     rsp = urllib2.urlopen(req)
#     content = rsp.read()
#     print "content is", content

URI_INITNODE = 'initnode'

BANDWIDTH_CAPACITY = "capacity"
CLOUDLET_NAME = 'cloudletName'

def initNode(capacity, localip):
    uri = URI_INITNODE
    params = dict()
    params[BANDWIDTH_CAPACITY] = capacity
    params[CLOUDLET_NAME] = localip
    print params
    ret = sendReq(uri, params)
    return ret

def createTree(appname, streamName, streamCapacity):
    return '1'


def getIp():
    userHome = os.getenv("HOME")
    filepath = userHome + '/ip'
    ipFile = open(filepath, 'r')
    ipList = []
    for line in ipFile:
        ipList.append(line.rstrip())
    return ipList
