from liveStreaming import streamMonitor
import subprocess
import os

ffmpegPath = '/home/ubuntu/ffmpeg-git-20141123-64bit-static/ffmpeg'

def openRtmp(appName, streamName, srcip):
    protocol = 'rtmp'
    port = 1935
    srcStream = appName + '/' + streamName
    tgtStream = appName + '/' + streamName
    pid = open(protocol, srcStream, tgtStream, srcip, port)
    return pid


def openRtsp(appName, streamName, srcip):
    protocol = 'rtsp'
    port = 1234
    srcStream = ''
    tgtStream = appName + '/' + streamName
    pid = open(protocol, srcStream, tgtStream, srcip, port)
    return pid


def close(pid):
    os.kill(int(pid), signal.SIGTERM)

def open(protocol, srcStream, tgtStream, srcip, port):
    src = protocol + '://' + srcip + ':' + str(port) + '/' + srcStream
    end = 'rtmp://127.0.0.1/' + tgtStream
    currQuality = streamMonitor.getCurrentQuality()
    command = [ffmpegPath, '-f', 'live_flv', '-re', '-i',
    src, '-s', currQuality, '-vcodec', 'libx264', '-f',
    'flv', end]
    print command
    proc = subprocess.Popen(command, shell=False)
    pid = proc.pid
    return pid
