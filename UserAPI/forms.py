from django.utils.translation import ugettext
from django import forms
from POCWebServiceAPI.admininfo import *
from django.contrib.auth import get_user_model
User = get_user_model()


class AddAdminForm(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobile = forms.CharField(required=True)
    date_of_birth = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    user_img = forms.ImageField(required=True)
    status = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'mobile', 'date_of_birth', 'user_img', 'status', 'password',
                  'confirm_password')

    def clean(self):
        cleaned_data = super(AddAdminForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        mobile = cleaned_data.get("mobile")
        if password != confirm_password:
            raise forms.ValidationError(ugettext("password and confirm password does not match"))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(ugettext("username already exist"))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(ugettext("Email already exist"))
        if User.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError(ugettext("Mobile number already exist"))
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', 'email')

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(ugettext("User is not Valid"))


class EditUserForm(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobile = forms.CharField(required=True)
    date_of_birth = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    status = forms.CharField(required=True)
    user_img = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'mobile', 'date_of_birth', 'email', 'status', 'user_img')

    def clean(self):
        cleaned_data = super(EditUserForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if not User.objects.filter(username=username, email=email).exists():
            raise forms.ValidationError(
                ugettext("User is not Valid")
            )
        return cleaned_data
