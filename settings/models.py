from django.db import models
from UserAPI.models import *

# Create your models here.
jsondata = eval(open("config/adminappconfig/config.json", "rb").read().decode())


class LogoFavIconsModel(models.Model):
    slug = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    field_type = models.CharField(max_length=200)
    manager = models.CharField(max_length=200)
    favlogo_value = models.CharField(max_length=200, unique=True, default="1_favlogo_value")
    config_value_file = models.FileField(upload_to="LogoFav/")
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)


class AddGeneralSettingModel(models.Model):
    title = models.CharField(max_length=200)
    Constant_Slug = models.CharField(max_length=200)
    field_type = models.CharField(max_length=200, default="text")
    config_value_bool = models.BooleanField(null=True)
    config_value_text = models.TextField(null=True)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)


class SMTPDetailModel(models.Model):
    SMTP_EMAIL = models.EmailField(max_length=200, null=False, default=jsondata["SMTP_EMAIL"])
    SMTPPASSWORD = models.TextField(max_length=2000, null=False, default=jsondata["SMTPPASSWORD"])
    SMTPPORT = models.IntegerField(null=False, default=jsondata["SMTPPORT"])
    SMTPUSERNAME = models.CharField(max_length=100, null=False, default=jsondata["SMTPUSERNAME"])
    SMTP_ALLOW = models.BooleanField(default=True)
    SMTPTLS = models.BooleanField(default=False)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now_add=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)


class SocialURLsModel(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    social_value = models.CharField(max_length=200, unique=True, default="0_socialvalue")
    url = models.TextField(max_length=5000)
    icon_class = models.CharField(max_length=200)
    field_type = models.CharField(max_length=200, default="text")
    manager = models.CharField(max_length=200, default="social")
    createat = models.DateTimeField(auto_now_add=True)
    updateat = models.DateTimeField(auto_now_add=True)
