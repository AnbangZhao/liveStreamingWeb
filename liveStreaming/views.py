from django.http import HttpResponse
from django.shortcuts import render
from config import CONFIG
from django.views.decorators.csrf import csrf_exempt
from streams.models import FfmpegStream
from streams.models import videoQuality
import subprocess
import urllib
import urllib2
import os
import signal
import socket
import random
from time import sleep

qualityTuple = ('1280x720', '640x480', '320x240')

def startup():
    FfmpegStream.objects.all().delete()
    videoQuality.objects.all().delete()
    array = FfmpegStream.objects.all()
    print len(array)

startup()

def home(request):
    queryDict = request.GET
    #myip = socket.gethostbyname(socket.gethostname())
    myip = '128.2.213.111'
    print myip
    appname = queryDict.__getitem__(CONFIG['appname'])
    streamname = queryDict.__getitem__(CONFIG['stream'])
    #return HttpResponse(socket.gethostbyname(socket.gethostname()))
    treename = getTreeName(appname, streamname)
    streamInfoArray = FfmpegStream.objects.filter(ftreename = treename)
    if len(streamInfoArray) >= 1:
        print "len is bigger than one"	
        return render(request, 'test.html', {'ip':myip, 'appname':appname, 'streamname':streamname})

    #ip = joinTree(appname, streamname)
    ip = '10.2.11.6'
    openStream(appname, streamname, ip, False)
    return render(request, 'test.html', {'ip':myip, 'appname':appname, 'streamname':streamname})

# open ffmpeg connection
# only allow get request
@csrf_exempt
def open(request):
    #if(request.method == 'GET') :
     #   return HttpResponse('GET not supported')

    queryDict = request.GET
    username = queryDict.__getitem__(CONFIG['username'])
    appname = queryDict.__getitem__(CONFIG['appname'])
    stream = queryDict.__getitem__(CONFIG['stream'])
    ip = queryDict.__getitem__(CONFIG['clientIP'])
    capacity = queryDict.__getitem__(CONFIG['streamCapacity'])
    openStream(appname, streamname, ip, True)

    createTree(appname, stream, capacity)

    tmpObj = FfmpegStream.objects.filter(ftreename = treeName)
    return HttpResponse(tmpObj[0].fpid)

# only allow get request
# for viewers to call
@csrf_exempt
def exit(request):
    queryDict = request.GET
    username = queryDict.__getitem__(CONFIG['username'])
    appname = queryDict.__getitem__(CONFIG['appname'])
    stream = queryDict.__getitem__(CONFIG['stream'])
    treeName = getTreeName(appname, stream)
    tmpObj = FfmpegStream.objects.filter(ftreename = treeName)
    userCount = int(tmpObj[0].fuserCount)
    pid = int(tmpObj[0].fpid)
    rtspSource = tmpObj[0].fRtspSource
    userCount -= 1
    newObj = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount, fRtspSource = rtspSource)
    newObj.save()
    if userCount <=0 :
        exitTree(appname, streamName)
        os.kill(pid, signal.SIGTERM)
    return HttpResponse(tmpObj[0].fpid)

# only allow get request
# for viewers to call
@csrf_exempt
def stop(request):
    queryDict = request.GET
    username = queryDict.__getitem__(CONFIG['username'])
    appname = queryDict.__getitem__(CONFIG['appname'])
    stream = queryDict.__getitem__(CONFIG['stream'])
    treeName = getTreeName(appname, stream)
    tmpObj = FfmpegStream.objects.filter(ftreename = treeName)
    userCount = int(tmpObj[0].fuserCount)
    pid = int(tmpObj[0].fpid)
    rtspSource = tmpObj[0].fRtspSource
    userCount -= 1
    newObj = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount, fRtspSource = rtspSource)
    newObj.save()
    exitTree(appname, streamName)
    os.kill(pid, signal.SIGTERM)

def degrade(request):
    currQuality = getCurrentQuality()
    index = qualityTuple.index(currQuality)
    if index == len(qualityTuple) - 1:
        return HttpResponse(currQuality)

    print index
    index += 1
    newQuality = qualityTuple[index]
    print 'newQuality', newQuality
    newObj = videoQuality(sVideo = 'video', sQuality = newQuality)
    newObj.save()
    for streamObj in FfmpegStream.objects.all():
        restart(streamObj, newQuality)
    return HttpResponse(newQuality)

def restart(streamObj, newQuality):
    treeName = streamObj.ftreename
    pid = streamObj.fpid
    rtspSource = streamObj.fRtspSource
    userCount = streamObj.fuserCount
    rtmpEnd = 'rtmp://127.0.0.1/' + treeName
    print 'restart pid: ' + pid
    print 'restart quality: ' + newQuality
    os.kill(int(pid), signal.SIGTERM)
    sleep(1)
    proc = subprocess.Popen(['/home/ubuntu/ffmpeg-git-20141123-64bit-static/ffmpeg', '-i', 
    rtspSource, '-s', newQuality, '-vcodec', 'libx264', '-strict', '-2', '-acodec', 'aac',  '-b:a', '32k','-f',
    'flv', rtmpEnd], shell=False)
    pid = proc.pid
    newObject = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount, fRtspSource = rtspSource)
    newObject.save()


def getCurrentQuality():
    objArray = videoQuality.objects.filter(sVideo = 'video')
    if len(objArray) == 0:
        print 'not none'
        quality = qualityTuple[0]
        newObj = videoQuality(sVideo = 'video', sQuality = quality)
        newObj.save()
        return quality
    return objArray[0].sQuality

def createTree(appname, streamName, streamCapacity):
    treeName = getTreeName(appname, streamName)
    createTreeUrl = "https://p2p-meta-server.appspot.com/createtree"
    values = dict(treename=treeName, consume=streamCapacity)
    data = urllib.urlencode(values)
    req = urllib2.Request(createTreeUrl, data)
    rsp = urllib2.urlopen(req)
    content = rsp.read()
    print "content is", content

def exitTree(appName, streamName):
    treeName = getTreeName(appname, streamName)
    createTreeUrl = "https://p2p-meta-server.appspot.com/createtree"
    values = dict(treename=treeName)
    req = urllib2.Request(createTreeUrl, data)
    rsp = urllib2.urlopen(req)
    content = rsp.read()
    print "content is", content

def openStream(appName, streamName, ip, isRtsp):
    treeName = getTreeName(appName, streamName)
    protocol = 'rtmp://'
    port = ''
    srcName = '/liveStreaming' + '/' + streamName
    if isRtsp == True:
        protocol = 'rtsp'
        port = ':1234'
        srcName = ''
    rtspSource = protocol + ip + port + srcName
    rtmpEnd = 'rtmp://127.0.0.1/liveStreaming' + '/' + streamName 
    currQuality = getCurrentQuality()
    proc = subprocess.Popen(['/home/ubuntu/ffmpeg-git-20141123-64bit-static/ffmpeg', '-i', 
    rtspSource, '-s', currQuality, '-vcodec', 'libx264', '-strict', '-2', '-acodec', 'aac',  '-b:a', '32k','-f',
    'flv', rtmpEnd], shell=False)
    #pid = 10086  
    pid = proc.pid
    print 'pid in openstream ' + str(pid)
    userCount = 1

    streamObject = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount, fRtspSource = rtspSource)
    streamObject.save()

def getTreeName(appname, streamName):
    treename = appname + "/" + streamName
    return treename

def joinTree(appname, streamname):
    treename = getTreeName(appname, streamname)
    createTreeUrl = "https://p2p-meta-server.appspot.com/jointree"
    values = dict(treename=treename)
    data = urllib.urlencode(values)
    req = urllib2.Request(createTreeUrl, data)
    rsp = urllib2.urlopen(req)
    content = rsp.read()
    return content

def getConnNum(appName, streamName):
    queryUrl = "http://127.0.0.1/stat"
    req = urllib2.Request(createTreeUrl, data)
    rsp = urllib2.urlopen(req)
    content = rsp.read()
    randNum = random.randrange(1, 10000)
    fileName = 'tmp.dat' + str(randNum)
    dataFile = open('tmp.dat', 'w')
    dataFile.write(content)
    dataFile.close()
    getNumFromXml(appName, streamName, fileName)
