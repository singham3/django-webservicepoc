from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
import json



class User(AbstractUser):
    mobile = models.CharField(max_length=20, unique=True)
    dateofbirth = models.DateTimeField()
    ismobile = models.BooleanField(default=False)
    isemail = models.BooleanField(default=False)
    userimg = models.ImageField(upload_to="media/")
    updatedat = models.DateTimeField(auto_now=True)
    loginBrowser = models.CharField(max_length=200, null=True)
    loginip = models.CharField(max_length=100, null=True)
    account_id = models.IntegerField(unique=True)
    token = models.TextField(max_length=65000)
    key = models.CharField(max_length=20,null=True)
    REQUIRED_FIELDS = ['email','mobile','dateofbirth','ismobile','isemail','userimg','updatedat','loginBrowser','loginip','account_id','key']









