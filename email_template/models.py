from UserAPI.models import *
from django.db import models


class AddEmailHooksModel(models.Model):
    title = models.CharField(max_length=200, unique=True)
    hook = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    status = models.BooleanField(default=False)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
