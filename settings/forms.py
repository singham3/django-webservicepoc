from django import forms
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class GeneralSettingForm(forms.Form):
    title = forms.CharField(required=True)
    Constant_Slug = forms.CharField(required=True)
    field_type = forms.CharField(required=True)
    setting_checkbox = forms.CharField(required=False)
    config_value = forms.CharField(required=False)

    class Meta:
        model = AddGeneralSettingModel
        fields = ('title', 'Constant_Slug', 'field_type', 'setting_checkbox')

    def clean(self):
        return super(GeneralSettingForm, self).clean()


class SMTPDetailForm(forms.Form):
    SMTP_ALLOW = forms.CharField(required=False)
    SMTP_EMAIL = forms.EmailField(required=True)
    SMTPPASSWORD = forms.CharField(required=True)
    SMTPUSERNAME = forms.CharField(required=True)
    SMTPPORT = forms.IntegerField(required=True)
    SMTP_TLS = forms.CharField(required=False)

    class Meta:
        model = SMTPDetailModel
        fields = ("SMTP_ALLOW", "SMTP_EMAIL", "SMTPPASSWORD", "SMTPUSERNAME", "SMTPPORT", "SMTP_TLS")

    def clean(self):
        return super(SMTPDetailForm, self).clean()


class SocialURLsForm(forms.Form):
    title = forms.CharField(required=True)
    url = forms.CharField(required=True)
    icon = forms.CharField(required=True)
    field_type = forms.CharField(required=True)
    manager = forms.CharField(required=True)
    social_value = forms.CharField(required=True)

    class Meta:
        model = SocialURLsModel
        fields = ("title", "url", "icon", "field_type", "manager", "manager", "social_value")