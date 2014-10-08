from django.http import HttpResponse
from django.shortcuts import render
from config import CONFIG
from django.views.decorators.csrf import csrf_exempt
from streams.models import FfmpegStream
import subprocess

def home(request):
    return render(request, 'test.html', {})

# open ffmpeg connection
# only allow post request
@csrf_exempt
def open(request):
    #if(request.method == 'GET') :
     #   return HttpResponse('GET not supported')

    queryDict = request.GET
    username = queryDict.__getitem__(CONFIG['username'])
    appname = queryDict.__getitem__(CONFIG['appname'])
    stream = queryDict.__getitem__(CONFIG['stream'])
    ip = queryDict.__getitem__(CONFIG['clientIP'])
    rtspSource = 'rtsp://' + ip + ':1234'
    rtmpEnd = 'rtmp://128.2.213.103/liveStreaming' + '/' + stream 

    streamObject = FfmpegStream(fip = ip, fstream = stream, fapp = appname)
    streamObject.save()
    subprocess.Popen(['/Users/anbang/Documents/development/django/liveStreaming/ffmpeg', '-i', 
        rtspSource, '-vcodec', 'libx264', '-strict', '-2', '-acodec', 'aac',  '-b:a', '32k','-f',
        'flv', rtmpEnd], shell=False)

    tmpObj = FfmpegStream.objects.filter(fip = ip, fstream = stream, fapp = appname)
    return HttpResponse(tmpObj[0].fip)