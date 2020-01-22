from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime
from POCWebServiceAPI.hashers import *


class CreateFavLgoService(Service):
    slug = forms.CharField()
    title = forms.CharField()
    field_type = forms.CharField()
    manager = forms.CharField()
    favlogo_value = forms.CharField()
    config_value_file = forms.FileField(required=False)
    userid = forms.CharField()

    def process(self):
        if LogoFavIconsModel.objects.filter(favlogo_value=self.cleaned_data['favlogo_value']).exists():
            lfdata = LogoFavIconsModel.objects.get(favlogo_value=self.cleaned_data['favlogo_value'])
            lfdata.slug = self.cleaned_data['slug']
            lfdata.title = self.cleaned_data['title']
            lfdata.field_type = self.cleaned_data['field_type']
            lfdata.manager = self.cleaned_data['manager']
            lfdata.updatedat = datetime.now()
            if self.cleaned_data['config_value_file']:
                lfdata.config_value_file = self.cleaned_data['config_value_file']
            lfdata.save()
        else:
            lfdb = LogoFavIconsModel(slug=self.cleaned_data['slug'], title=self.cleaned_data['title'],
                                     favlogo_value=self.cleaned_data['favlogo_value'],
                                     field_type=self.cleaned_data['field_type'],
                                     manager=self.cleaned_data['manager'],
                                     config_value_file=self.cleaned_data['config_value_file'],
                                     userid=User.objects.get(account_id=self.cleaned_data['userid']))
            lfdb.save()


class CreateGenSettingService(Service):
    title = forms.CharField()
    Constant_Slug = forms.CharField()
    field_type = forms.CharField()
    config_value = forms.CharField(widget=forms.Textarea, required=False)
    userid = forms.CharField()

    def process(self):
        if self.cleaned_data['config_value'] == '' or self.cleaned_data['config_value'] is None:
            AddGeneralSettingModel.objects.create(title=self.cleaned_data['title'],
                                                  Constant_Slug=self.cleaned_data['Constant_Slug'],
                                                  field_type=self.cleaned_data['field_type'],
                                                  config_value_bool=False,
                                                  config_value_text=None,
                                                  userid=User.objects.get(account_id=self.cleaned_data['userid'])
                                                  )
        elif self.cleaned_data['config_value'] == "on":
            AddGeneralSettingModel.objects.create(title=self.cleaned_data['title'],
                                                  Constant_Slug=self.cleaned_data['Constant_Slug'],
                                                  field_type=self.cleaned_data['field_type'],
                                                  config_value_bool=True,
                                                  config_value_text=None,
                                                  userid=User.objects.get(account_id=self.cleaned_data['userid'])
                                                  )
        else:
            AddGeneralSettingModel.objects.create(title=self.cleaned_data['title'],
                                                  Constant_Slug=self.cleaned_data['Constant_Slug'],
                                                  field_type=self.cleaned_data['field_type'],
                                                  config_value_bool=None,
                                                  config_value_text=self.cleaned_data['config_value'],
                                                  userid=User.objects.get(account_id=self.cleaned_data['userid'])
                                                  )


class EditGenSettingService(Service):
    gs_id = forms.CharField()
    title = forms.CharField()
    Constant_Slug = forms.CharField()
    field_type = forms.CharField()
    config_value = forms.CharField(widget=forms.Textarea, required=False)

    def process(self):
        gs_data = AddGeneralSettingModel.objects.get(id=self.cleaned_data['gs_id'])
        gs_data.title = self.cleaned_data['title']
        gs_data.Constant_Slug = self.cleaned_data['Constant_Slug']
        gs_data.field_type = self.cleaned_data['field_type']
        if self.cleaned_data['config_value'] == '' or self.cleaned_data['config_value'] is None:
            gs_data.config_value_bool = False
            gs_data.config_value_text = None
        elif self.cleaned_data['config_value'] == "on":
            gs_data.config_value_bool = True
            gs_data.config_value_text = None
        else:
            gs_data.config_value_bool = None
            gs_data.config_value_text = self.cleaned_data['config_value']
        gs_data.updatedat = datetime.now()
        gs_data.save()


class SMTPDetailService(Service):
    SMTP_ALLOW = forms.CharField(required=False)
    SMTP_EMAIL = forms.EmailField()
    SMTPPASSWORD = forms.CharField()
    SMTPUSERNAME = forms.CharField()
    SMTPPORT = forms.IntegerField()
    SMTP_TLS = forms.CharField(required=False)
    userid = forms.CharField()

    def process(self):
        try:
            smtpdb = SMTPDetailModel.objects.get()
            smtpdb.SMTP_EMAIL = self.cleaned_data['SMTP_EMAIL']
            smtpdb.SMTPPASSWORD = encrypt_message_rsa(self.cleaned_data['SMTPPASSWORD'], jsondata["publickey"])
            smtpdb.SMTPPORT = self.cleaned_data['SMTPPORT']
            smtpdb.SMTPUSERNAME = self.cleaned_data['SMTPUSERNAME']
            smtpdb.userid = User.objects.get(account_id=self.cleaned_data['userid'])
            if self.cleaned_data['SMTP_TLS'] == 'on':
                smtpdb.SMTPTLS = True
            else:
                smtpdb.SMTPTLS = False
            if self.cleaned_data['SMTP_ALLOW'] == 'on':
                smtpdb.SMTP_ALLOW = True
            else:
                smtpdb.SMTP_ALLOW = False
            smtpdb.updatedat = datetime.now()
            smtpdb.save()
        except:
            smtpdb = SMTPDetailModel(SMTP_EMAIL=self.cleaned_data['SMTP_EMAIL'],
                                     SMTPPASSWORD=encrypt_message_rsa(self.cleaned_data['SMTPPASSWORD'],
                                                                      jsondata["publickey"]),
                                     SMTPPORT=self.cleaned_data['SMTPPORT'],
                                     SMTPUSERNAME=self.cleaned_data['SMTPUSERNAME'],
                                     userid=User.objects.get(account_id=self.cleaned_data['userid']), )
            if self.cleaned_data['SMTP_TLS'] == 'on':
                smtpdb.SMTPTLS = True
            else:
                smtpdb.SMTPTLS = False
            if self.cleaned_data['SMTP_ALLOW'] == 'on':
                smtpdb.SMTP_ALLOW = True
            else:
                smtpdb.SMTP_ALLOW = False

            smtpdb.save()


class SocialURLsService(Service):
    userid = forms.CharField()
    title = forms.CharField()
    social_value = forms.CharField()
    url = forms.CharField()
    iconclass = forms.CharField()
    field_type = forms.CharField()
    manager = forms.CharField()

    def process(self):
        if SocialURLsModel.objects.filter(social_value=self.cleaned_data['social_value']).exists():
            sldata = SocialURLsModel.objects.get(social_value=self.cleaned_data['social_value'])
            sldata.title = self.cleaned_data['title']
            sldata.field_type = self.cleaned_data['field_type']
            sldata.manager = self.cleaned_data['manager']
            sldata.url = self.cleaned_data['url']
            sldata.icon_class = self.cleaned_data['iconclass']
            sldata.updateat = datetime.now()
            sldata.save()
        else:
            SocialURLsModel.objects.create(userid=User.objects.get(account_id=self.cleaned_data['userid']),
                                           title=self.cleaned_data['title'],
                                           url=self.cleaned_data['url'],
                                           icon_class=self.cleaned_data['iconclass'],
                                           field_type=self.cleaned_data['field_type'],
                                           manager=self.cleaned_data['manager'],
                                           social_value=self.cleaned_data['social_value'])