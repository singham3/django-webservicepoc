from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from random import randint
from datetime import datetime
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


class CmspagesConfig(AppConfig):
    name = 'secondaryDB'


cmsjsondata = eval(open("config/cmspageconfig/cmsconfig.json","r").read())
userjsondata = eval(open("config/adminappconfig/userconfig.json","r").read())


def create_CMSpages(sender, **kwargs):
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        userdata = User.objects.get(username="admin")
    except User.DoesNotExist:
        User.objects.create_superuser(username=userjsondata['username'], email=userjsondata['email'],
                                      first_name=userjsondata['first_name'], last_name=userjsondata['last_name'],
                                      is_superuser=bool(userjsondata['is_superuser']),
                                      is_staff=bool(userjsondata['is_staff']),
                                      is_active=bool(userjsondata['is_active']), mobile=userjsondata['mobile'],
                                      dateofbirth=datetime.strptime(userjsondata['dateofbirth'], '%m/%d/%Y'),
                                      userimg=userjsondata['userimg'],
                                      loginBrowser=userjsondata['loginBrowser'], loginip=str(IPAddr),
                                      account_id=randint(10 ** (8 - 1), (10 ** 8) - 1),
                                      password=userjsondata['password'])
        userdata = User.objects.get(username="admin")

    from .models import CMSpagemodel

    try:
        if CMSpagemodel.objects.count() == 0:
            CMSpagemodel.objects.get()
        else:
            CMSpagemodel.objects.filter()
    except CMSpagemodel.DoesNotExist:
        CMSpagemodel.objects.create(title=cmsjsondata['title'],
                                    meta_title=cmsjsondata['meta_title'],
                                    sub_title=cmsjsondata['sub_title'],
                                    meta_keyword=cmsjsondata['meta_keyword'],
                                    slug=cmsjsondata['slug'],
                                    meta_description=cmsjsondata['meta_description'],
                                    short_description=cmsjsondata['short_description'],
                                    cmsfile=cmsjsondata['cmsfile'],
                                    html_description=cmsjsondata['html_description'],
                                    userid=userdata,
                                    status=True)


class CMSpagesAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_CMSpages)
