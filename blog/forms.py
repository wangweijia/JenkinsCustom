from django import forms
from blog.models import *


class LoginForm(forms.Form):
    userName = forms.CharField(max_length=10)
    passWord = forms.CharField(max_length=10, widget=forms.PasswordInput)


class ProjectConfig(forms.Form):
    queue = forms.ModelChoiceField(label="新打包环境:", queryset=Config.objects.all(), to_field_name='configName')
