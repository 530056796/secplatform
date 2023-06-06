from django.db import models

# Create your models here.

from django.db import models

class Scaninfo(models.Model):
    taskid = models.CharField(max_length=32)
    taskname = models.CharField(max_length=64)
    appname = models.CharField(max_length=64)
    appid = models.CharField(max_length=64)
    starttime = models.CharField(max_length=32)
    endtime = models.CharField(max_length=32)
    Murl = models.CharField(max_length=128)
    Auth_Token = models.CharField(max_length=64)
    cftk = models.CharField(max_length=64)
    regex_str = models.CharField(max_length=516)
    taskbegintime = models.CharField(max_length=32)
    finishtime = models.CharField(max_length=32)
    progress = models.CharField(max_length=16)
    report = models.CharField(max_length=128)


