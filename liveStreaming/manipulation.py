from liveStreaming.httpService import *

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

def initNode(capacity):
    uri = URI_INITNODE
    params = dict()
    params[BANDWIDTH_CAPACITY] = capacity
    print params
    ret = sendReq(uri, params)
    return ret

def createTree(appname, streamName, streamCapacity):
    return '1'