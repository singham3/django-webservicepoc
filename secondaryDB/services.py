from service_objects.services import Service
from django import forms
from .models import *
from datetime import datetime


class CreateCMSPageService(Service):
    title = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    sub_title = forms.CharField(required=True)
    meta_keyword = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    short_description = forms.CharField(required=True)
    cms_file = forms.FileField(required=True)
    html_description = forms.CharField(widget=forms.Textarea, required=True)
    user_id = forms.CharField()

    def process(self):
        cms_db = CMSpagemodel(title=self.cleaned_data["title"], meta_title=self.cleaned_data["meta_title"],
                              sub_title=self.cleaned_data["sub_title"], meta_keyword=self.cleaned_data["meta_keyword"],
                              slug=self.cleaned_data["slug"], meta_description=self.cleaned_data["meta_description"],
                              userid=User.objects.get(account_id=self.cleaned_data["user_id"]),
                              cmsfile=self.cleaned_data["cms_file"],
                              short_description=self.cleaned_data["short_description"], createdate=datetime.now(),
                              html_description=self.cleaned_data["html_description"], updatedate=datetime.now())
        cms_db.save()


class EditCMSPageService(Service):
    title = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    sub_title = forms.CharField(required=True)
    meta_keyword = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    short_description = forms.CharField(required=True)
    cms_file = forms.FileField(required=False)
    cms_id = forms.CharField(required=True)
    html_description = forms.CharField(widget=forms.Textarea, required=True)

    def process(self):
        cms_data = CMSpagemodel.objects.get(id=self.cleaned_data["cms_id"])
        cms_data.title = self.cleaned_data["title"]
        cms_data.meta_title = self.cleaned_data["meta_title"]
        cms_data.sub_title = self.cleaned_data["sub_title"]
        cms_data.meta_keyword = self.cleaned_data["meta_keyword"]
        cms_data.slug = self.cleaned_data["slug"]
        cms_data.meta_description = self.cleaned_data["meta_description"]
        cms_data.short_description = self.cleaned_data["short_description"]
        cms_data.html_description = self.cleaned_data["html_description"]
        print(self.cleaned_data["cms_file"])
        if self.cleaned_data["cms_file"]:
            cms_data.cmsfile = self.cleaned_data["cms_file"]
        cms_data.updatedate = datetime.now()
        cms_data.save()

