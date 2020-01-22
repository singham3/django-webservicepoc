from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime


class CreateEmailHookService(Service):
    title = forms.CharField()
    hook = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    status = forms.CharField()
    userid = forms.CharField()

    def process(self):
        email_hook_db = AddEmailHooksModel(title=self.cleaned_data['title'], hook=self.cleaned_data['hook'],
                                           description=self.cleaned_data['description'],
                                           status=bool(self.cleaned_data['status']),
                                           userid=User.objects.get(account_id=self.cleaned_data['userid']))
        email_hook_db.save()
