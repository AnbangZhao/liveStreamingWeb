from django.db import models

class publisher(models.Model) :
    name = models.CharField(max_length = 30)
    stream = models.CharField(max_length = 100)

class FfmpegStream(models.Model) :
    fip = models.CharField(max_length = 30)
    fstream = models.CharField(max_length = 30)
    fapp = models.CharField(max_length = 30)