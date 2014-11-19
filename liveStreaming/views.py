from django.http import HttpResponse
from django.shortcuts import render
from config import CONFIG
from django.views.decorators.csrf import csrf_exempt
from streams.models import FfmpegStream
import subprocess
import urllib
import urllib2
import os
import signal
import socket

def home(request):
    queryDict = request.GET
    myip = socket.gethostbyname(socket.gethostname())
    appname = queryDict.__getitem__(CONFIG['appname'])
    streamname = queryDict.__getitem__(CONFIG['stream'])
    #return HttpResponse(socket.gethostbyname(socket.gethostname()))
    treename = getTreeName(appname, streamname)
    streamInfoArray = FfmpegStream.objects.filter(ftreename = treename)
    #if len(streamInfoArray) >= 1:
     #   return render(request, 'test.html', {'ip':myip, 'appname':appname, 'streamname':streamname})

    con = joinTree(appname, streamname)
    return con
    #return render(request, 'test.html', {'ip':myip, 'appname':appname, 'streamname':streamname})

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
    rtspSource = 'rtsp://' + ip + ':1234'
    rtmpEnd = 'rtmp://127.0.0.1/liveStreaming' + '/' + stream 

    treeName = getTreeName(appname, stream)
    #proc = subprocess.Popen(['/Users/anbang/Documents/development/django/liveStreaming/ffmpeg', '-i', 
      #  rtspSource, '-vcodec', 'libx264', '-strict', '-2', '-acodec', 'aac',  '-b:a', '32k','-f',
        #'flv', rtmpEnd], shell=False)

    #pid = proc.pid
    pid = 10086
    userCount = 1

    streamObject = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount)
    streamObject.save()

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
    userCount -= 1
    newObj = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount)
    newObj.save()
    if userCount <=0 :
        exitTree(appname, streamName)
        os.killpg(pid, signal.SIGTERM)
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
    userCount -= 1
    newObj = FfmpegStream(ftreename = treeName, fpid = pid, fuserCount = userCount)
    newObj.save()
    exitTree(appname, streamName)
    os.killpg(pid, signal.SIGTERM)

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
