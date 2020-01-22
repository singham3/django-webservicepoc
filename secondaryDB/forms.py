from django import forms
from django.contrib.auth import get_user_model
from .models import CMSpagemodel

User = get_user_model()


class CMSPageForm(forms.Form):
    title = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    sub_title = forms.CharField(required=True)
    meta_keyword = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    short_description = forms.CharField(required=True)
    cms_file = forms.FileField(required=False)
    html_description = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = CMSpagemodel
        fields = ('title', 'meta_title', 'sub_title', 'meta_keyword', 'slug', 'meta_description', 'short_description',
                  'cms_file', 'html_description')

    def clean(self):
        return super(CMSPageForm, self).clean()
