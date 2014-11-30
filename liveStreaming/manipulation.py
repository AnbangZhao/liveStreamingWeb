from liveStreaming.httpService import *
from liveStreaming import ffmpeg
from streams.models import FfmpegStream
import os

URI_INITNODE = 'initnode'

BANDWIDTH_CAPACITY = "capacity"
CLOUDLET_NAME = 'cloudletName'
TREE_NAME = 'treename'
STREAM_CAPACITY = 'consume'

def initNode(capacity, localip):
    uri = URI_INITNODE
    params = dict()
    params[BANDWIDTH_CAPACITY] = capacity
    params[CLOUDLET_NAME] = localip
    ret = sendReq(uri, params)
    return ret

def createTree(appName, streamName, streamCapacity, localip, clientIP):
    treeName = getTreeName(appName, streamName)
    uri = "createtree"
    params = dict()
    params[TREE_NAME] = treeName
    params[STREAM_CAPACITY] = streamCapacity
    params[CLOUDLET_NAME] = localip
    retCode = sendReq(uri, params)

    #pid = ffmpeg.openRtsp(appName, streamName, clientIP)
    # for now. To be changed to rtsp
    pid = ffmpeg.openRtmp(appName, streamName, clientIP)

    userCount = 1
    position = 'root'
    streamObject = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount, fposition = position)
    streamObject.save()


def exitTree(appName, streamName, localip):
    #clean data structure in metadata server 
    treeName = getTreeName(appname, streamName)
    uri = "exittree"
    params = dict(treename=treeName)
    params[CLOUDLET_NAME] = localip
    retCode = sendReq(uri, params)
    # if return value is 409, means there's new node
    # don't exit the pipe
    if retCode == 202:
        return

    # clean local data
    ffmpegArray = FfmpegStream.objects.filter(ftreename = treeName)
    if len(ffmpegArray) == 0:
        return
    ffmpegObj = ffmpegArray[0]
    pid = ffmpegObj.fpid
    ffmpegObj.delete()

    #close ffmpeg
    ffmpeg.close(pid)


def getIp():
    userHome = os.getenv("HOME")
    filepath = userHome + '/ip'
    ipFile = open(filepath, 'r')
    ipList = []
    for line in ipFile:
        ipList.append(line.rstrip())
    return ipList

def getTreeName(appname, streamName):
    treename = appname + "/" + streamName
    return treename
