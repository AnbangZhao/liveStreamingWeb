from django.db import models

class publisher(models.Model) :
    name = models.CharField(max_length = 30, primary_key=True)
    stream = models.CharField(max_length = 100)

class FfmpegStream(models.Model) :
    ftreename = models.CharField(max_length = 50, primary_key=True)
    fpid = models.CharField(max_length = 10)
    fuserCount = models.CharField(max_length = 10)