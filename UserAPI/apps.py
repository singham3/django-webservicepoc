from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth.apps import AuthConfig
from random import randint
from datetime import datetime
import socket


class UserapiConfig(AppConfig):
    name = 'UserAPI'


hostname = socket.gethostname()
IPAddress = socket.gethostbyname(hostname)


user_json_data = eval(open("config/adminappconfig/userconfig.json", "r").read())


def create_test_user(sender, **kwargs):
    if not settings.DEBUG:
        return
    if not isinstance(sender, AuthConfig):
        return
    from django.contrib.auth import get_user_model
    user = get_user_model()
    manager = user.objects
    try:
        manager.get(username="admin")
    except user.DoesNotExist:
        manager.create_superuser(username=user_json_data['username'], email=user_json_data['email'],
                                 first_name=user_json_data['first_name'], last_name=user_json_data['last_name'],
                                 is_superuser=bool(user_json_data['is_superuser']),
                                 is_staff=bool(user_json_data['is_staff']), is_active=bool(user_json_data['is_active']),
                                 mobile=user_json_data['mobile'],
                                 dateofbirth=datetime.strptime(user_json_data['date_of_birth'], '%m/%d/%Y'),
                                 userimg=user_json_data['user_img'],
                                 loginBrowser=user_json_data['loginBrowser'], loginip=str(IPAddress),
                                 account_id=randint(10 ** (8 - 1), (10 ** 8) - 1), password=user_json_data['password'])


class ExampleAppConfig(AppConfig):
    name = __package__

    def ready(self):
        post_migrate.connect(create_test_user)
