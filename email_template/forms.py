from django import forms
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class AddEmailHookForm(forms.Form):
    title = forms.CharField(required=True)
    hook = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.CharField(required=True)

    class Meta:
        model = AddEmailHooksModel
        fields = ('title', 'hook', 'description', 'status')

    def clean(self):
        return super(AddEmailHookForm, self).clean()
