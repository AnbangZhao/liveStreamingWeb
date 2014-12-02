from liveStreaming.httpService import *
from liveStreaming import ffmpeg
from streams.models import FfmpegStream
import os
import time

URI_INITNODE = 'initnode'

BANDWIDTH_CAPACITY = "capacity"
CLOUDLET_NAME = 'cloudletName'
TREE_NAME = 'treename'
STREAM_CAPACITY = 'consume'
MAX_DURATION = 25

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
    retTuple = sendReq(uri, params)

    #pid = ffmpeg.openRtsp(appName, streamName, clientIP)
    # for now. To be changed to rtsp
    pid = ffmpeg.openRtmp(appName, streamName, clientIP)

    userCount = 1
    position = 'root'
    currTime = time.time()
    streamObject = FfmpegStream(ftreename = treeName, fsrcip = clientIP, fpid = pid, fuserCount = userCount, fposition = position, ftime = currTime)
    streamObject.save()


def exitTree(appName, streamName, localip):
    #clean data structure in metadata server 
    treeName = getTreeName(appName, streamName)
    uri = "exittree"
    params = dict(treename=treeName)
    params[CLOUDLET_NAME] = localip
    retTuple = sendReq(uri, params)
    retCode = retTuple[0]
    # if return value is 202, means there's new node
    # don't exit the pipe
    if retCode == 202:
        print 'retCode is 202'
        return

    # clean local data
    ffmpegArray = FfmpegStream.objects.filter(ftreename = treeName)
    if len(ffmpegArray) == 0:
        print 'ffmpegArray length is 0'
        return
    ffmpegObj = ffmpegArray[0]
    pid = ffmpegObj.fpid
    ffmpegObj.delete()

    #close ffmpeg
    print 'deleting the ffmpeg with pid', pid
    ffmpeg.close(pid)


def connectStream(appName, streamName, localip):
    treeName = getTreeName(appName, streamName)
    streamInfoArray = FfmpegStream.objects.filter(ftreename = treeName)
    currTime = time.time()
    # there is already an ffmpeg pipe
    if len(streamInfoArray) >= 1:
        print "stream is already connected"
        streamObj = streamInfoArray[0]
        streamObj.update(ftime = currTime)
        return

    #  add into the stream tree in metadata server
    srcip = joinTree(appName, streamName, localip)
    if srcip == None:
        return

    # open ffmpeg pipe
    pid = ffmpeg.openRtmp(appName, streamName, srcip)

    # modify internal data structure
    position = 'nonroot'
    streamObject = FfmpegStream(ftreename = treeName, fsrcip = srcip, fpid = pid, fposition = position, ftime = currTime)
    streamObject.save()


def dealNoViewer(appName, streamName, localip):
    treeName = getTreeName(appName, streamName)
    streamInfoArray = FfmpegStream.objects.filter(ftreename = treeName)
    # if no such stream in db, do nothing
    if len(streamInfoArray) == 0:
        return
    streamObj = streamInfoArray[0]
    # if it's a new stream, do nothing
    # if this node is root, do nothing
    if isNewStream(streamObj) == True or isRoot(streamObj):
        print 'it\'s new stream or root'
        return
    # otherwise, this is a non-root node with no viewers. Safely exit it
    else:
        exitTree(appName, streamName, localip)

def checkStream(treeName):
    streamInfoArray = FfmpegStream.objects.filter(ftreename = treeName)
    if len(streamInfoArray) == 0:
        return 'up'
    else:
        return 'down'


def dealError(appName, streamName, rootStatus, localip):
    treeName = getTreeName(appName, streamName)
    streamInfoArray = FfmpegStream.objects.filter(ftreename = treeName)
    # if no such stream in db, do nothing
    if len(streamInfoArray) == 0:
        return
    streamObj = streamInfoArray[0]
    # if it's a new stream, do nothing and return
    if isNewStream(streamObj):
        print 'new stream error'
        return

    #if it's an old root, exit it
    if isRoot(streamObj):
        print 'old root error. exit'
        exitTree(appName, streamName, localip)
    else:
        #if this is a non-root and the root of the 
        #stream is down. exit it
        if rootStatus == 'down':
            exitTree(appName, streamName, localip)
        #if this is a non-root and the root is good
        #check connectivity with the previous node
        else:
            prevIP = getPrevIP(streamObj)
            prevStatus = getStreamStatus(prevIP, treeName)
            print 'prevStatus is', prevStatus
            #if the prev node has good stream, do nothing
            if prevStatus == 'up':
                return
            #if the prev node does not have a good stream or waiting
            #reconnect
            else:
                reConnectStream(appName, streamName, streamObj, localip)


# private methods#

def reConnectStream(appName, streamName, streamObj, localip):
    #reschedule in metadata server and get a new ip address
    newSrcip = joinTree(appName, streamName, localip)
    #close the old pipe
    oldPid = streamObj.fpid
    ffmpeg.close(oldPid)
    #open a new rtmp pipe (this node is guaranteed not to be root)
    newPid = ffmpeg.openRtmp(appName, streamName, newSrcip)
    #update local data structure
    #srcip pid ftime
    currTime = time.time()
    streamObj.update(fsrcip = newSrcip)
    streamObj.update(fpid = newPid)
    streamObj.update(ftime = currTime)

def getStreamStatus(ip, treeName):
    url = "http://" + ip + ":8000/check"
    params = dict(treename=treeName)
    print 'url', url
    print 'params', params
    data = urllib.urlencode(params)
    req = urllib2.Request(url, data)
    rsp = urllib2.urlopen(req)
    retCode = rsp.getcode()
    content = rsp.read()
    rsp.close()
    return content

def joinTree(appName, streamName, localip):
    treeName = getTreeName(appName, streamName)
    uri = "jointree"
    params = dict(treename=treeName)
    params[CLOUDLET_NAME] = localip
    retTuple = sendReq(uri, params)
    retCode = retTuple[0]
    retMessage = retTuple[1]
    # do nothing
    if retCode == 202:
        return None

    streamSrcIp = retMessage
    return streamSrcIp


def isNewStream(streamObj):
    arrivalTime = float(streamObj.ftime)
    currTime = time.time()
    duration = currTime - arrivalTime
    print 'time duration:', duration
    return duration < MAX_DURATION


def isRoot(streamObj):
    position = streamObj.fposition
    return position == 'root'


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

def getPrevIP(streamObj):
    srcip = streamObj.fsrcip
    print 'prev ip', srcip
    return srcip
