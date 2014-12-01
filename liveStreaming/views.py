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
from liveStreaming.manipulation import *
from liveStreaming.httpService import sendReq
from time import sleep


CLOUDLET_DEFAULT_CAPACITY = 1000
LOCALIP = ''
PUBLICIP = ''

def startup():
    FfmpegStream.objects.all().delete()
    videoQuality.objects.all().delete()
    ipList = getIp()
    global LOCALIP
    global PUBLICIP
    LOCALIP = ipList[0]
    PUBLICIP = ipList[1]
    initNode(CLOUDLET_DEFAULT_CAPACITY, LOCALIP)

startup()

def home(request):
    queryDict = request.GET
    appname = queryDict.__getitem__(CONFIG['appname'])
    streamname = queryDict.__getitem__(CONFIG['stream'])
    
    connectStream(appname, streamname, LOCALIP)
    return render(request, 'test.html', {'ip':PUBLICIP, 'appname':appname, 'streamname':streamname})

# open ffmpeg connection
# only allow get request
@csrf_exempt
def open(request):
    #if(request.method == 'GET') :
     #   return HttpResponse('GET not supported')

    queryDict = request.GET
    appname = queryDict.__getitem__(CONFIG['appname'])
    stream = queryDict.__getitem__(CONFIG['stream'])
    clientIP = queryDict.__getitem__(CONFIG['clientIP'])
    capacity = queryDict.__getitem__(CONFIG['streamCapacity'])
    #openStream(appname, streamname, ip, True)

    createTree(appname, stream, capacity, LOCALIP, clientIP)

    # tmpObj = FfmpegStream.objects.filter(ftreename = treeName)
    # return HttpResponse(tmpObj[0].fpid)
    return HttpResponse('open stream succeeded')

# only allow get request
# for viewers to call
@csrf_exempt
def exit(request):
    queryDict = request.GET
    appName = queryDict.__getitem__(CONFIG['appname'])
    streamName = queryDict.__getitem__(CONFIG['stream'])
    exitTree(appName, streamName, LOCALIP)

    return HttpResponse('exittree succeeded')

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


@csrf_exempt
def noviewer(request):
    queryDict = request.POST
    appName = queryDict.__getitem__(CONFIG['appname'])
    streamName = queryDict.__getitem__(CONFIG['stream'])
    dealNoViewer(appName, streamName, LOCALIP)
    return HttpResponse('success')

def restart(streamObj, newQuality):
    treeName = streamObj.ftreename
    pid = streamObj.fpid
    rtspSource = streamObj.fRtspSource
    userCount = streamObj.fuserCount
    rtmpEnd = 'rtmp://127.0.0.1/' + treeName
    print 'restart pid: ' + pid
    print 'restart quality: ' + newQuality
    os.kill(int(pid), signal.SIGTERM)
    sleep(2)
    proc = subprocess.Popen(['/home/ubuntu/ffmpeg-git-20141123-64bit-static/ffmpeg', '-f', 'live_flv','-i', 
    rtspSource, '-s', newQuality, '-map', '0:0','-vcodec', 'libx264','-f',
    'flv', rtmpEnd], shell=False)
    pid = proc.pid
    print "pid", pid
    newObject = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount, fRtspSource = rtspSource)
    newObject.save()





# def openStream(appName, streamName, ip, isRtsp):
#     treeName = getTreeName(appName, streamName)
#     protocol = 'rtmp://'
#     port = ''
#     srcName = '/liveStreaming' + '/' + streamName
#     if isRtsp == True:
#         protocol = 'rtsp'
#         port = ':1234'
#         srcName = ''
#     rtspSource = protocol + ip + port + srcName
#     rtmpEnd = 'rtmp://127.0.0.1/liveStreaming' + '/' + streamName 
#     currQuality = getCurrentQuality()
#     proc = subprocess.Popen(['/home/ubuntu/ffmpeg-git-20141123-64bit-static/ffmpeg', '-f', 'live_flv', '-re', '-i',
#     rtspSource, '-s', currQuality, '-vcodec', 'libx264', '-f',
#     'flv', rtmpEnd], shell=False)
#     #pid = 10086  
#     pid = proc.pid
#     print 'pid in openstream ' + str(pid)
#     userCount = 1

#     streamObject = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount, fRtspSource = rtspSource)
#     streamObject.save()

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
