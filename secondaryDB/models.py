from UserAPI.models import *
from django.db import models


class CMSpagemodel(models.Model):
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    meta_keyword = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    short_description = models.CharField(max_length=200)
    cmsfile = models.FileField(upload_to='cmspage/')
    html_description = models.TextField(max_length=65500)
    createdate = models.DateTimeField(auto_now_add=True)
    updatedate = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
