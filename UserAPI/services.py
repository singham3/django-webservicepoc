from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime
from random import randint


class CreateUserService(Service):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    mobile = forms.CharField()
    date_of_birth = forms.CharField()
    email = forms.EmailField()
    user_img = forms.FileField()
    status = forms.CharField()
    password = forms.CharField()
    browser_type = forms.CharField()
    user_ip = forms.CharField()

    def process(self):
        user_db = User(username=self.cleaned_data["username"], first_name=self.cleaned_data["first_name"],
                       is_superuser=bool(int(self.cleaned_data["status"])),
                       is_staff=bool(int(self.cleaned_data["status"])), last_name=self.cleaned_data["last_name"],
                       email=self.cleaned_data["email"], is_active=bool(int(self.cleaned_data["status"])),
                       mobile=self.cleaned_data["mobile"],
                       dateofbirth=datetime.strptime(self.cleaned_data["date_of_birth"], '%m/%d/%Y'),
                       ismobile=False, isemail=False, userimg=self.cleaned_data["user_img"],
                       loginBrowser=self.cleaned_data["browser_type"], loginip=self.cleaned_data["user_ip"],
                       account_id=randint(10 ** (8 - 1), (10 ** 8) - 1))
        user_db.set_password(self.cleaned_data["password"])
        user_db.save()


class EditUserService(Service):
    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    mobile = forms.CharField()
    account_id = forms.CharField()
    date_of_birth = forms.CharField()
    email = forms.EmailField()
    user_img = forms.FileField(required=False)
    password = forms.CharField(required=False)
    status = forms.CharField(required=False)
    browser_type = forms.CharField()
    user_ip = forms.CharField()

    def process(self):
        if User.objects.filter(account_id=int(self.cleaned_data['account_id']), username=self.cleaned_data['username'], 
                               email=self.cleaned_data['email']).exists():
            get_user_data = User.objects.get(account_id=int(self.cleaned_data['account_id']), 
                                             username=self.cleaned_data['username'], email=self.cleaned_data['email'])
            if self.cleaned_data['first_name']:
                get_user_data.first_name = self.cleaned_data['first_name']
            if self.cleaned_data['last_name']:
                get_user_data.last_name = self.cleaned_data['last_name']
            get_user_data.mobile = self.cleaned_data['mobile']
            get_user_data.dateofbirth = datetime.strptime(self.cleaned_data["date_of_birth"], '%m/%d/%Y')
            if self.cleaned_data['status']:
                get_user_data.is_active = bool(int(self.cleaned_data['status']))
                get_user_data.is_superuser = bool(int(self.cleaned_data['status']))
                get_user_data.is_staff = bool(int(self.cleaned_data['status']))
            get_user_data.loginBrowser = self.cleaned_data['browser_type']
            get_user_data.loginip = self.cleaned_data['user_ip']
            get_user_data.updatedat = datetime.now()
            if self.cleaned_data['user_img']:
                get_user_data.userimg = self.cleaned_data['user_img']
            if self.cleaned_data['password']:
                get_user_data.set_password(self.cleaned_data['password'])
            get_user_data.save()
