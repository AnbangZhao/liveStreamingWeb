from streams.models import videoQuality

qualityTuple = ('640x480', '480x360','320x240')

def getCurrentQuality():
    objArray = videoQuality.objects.filter(sVideo = 'video')
    if len(objArray) == 0:
        print 'default quality'
        quality = qualityTuple[0]
        newObj = videoQuality(sVideo = 'video', sQuality = quality)
        newObj.save()
        return quality
    return objArray[0].sQuality