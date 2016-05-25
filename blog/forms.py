from django import forms
from blog.models import *


class LoginForm(forms.Form):
    userName = forms.CharField(max_length=10)
    passWord = forms.CharField(max_length=10, widget=forms.PasswordInput)


# class ProjectConfig(forms.Form):
#     queue = forms.ModelChoiceField(label="新打包环境:", queryset=Config.objects.all(), to_field_name='configName')


class ProjectConfig(forms.Form):
    def __init__(self, projects):
        super(ProjectConfig, self).__init__()
        p = Project.objects.get(projectName=projects).id
        queue = forms.ModelChoiceField(label="新打包环境:", queryset=Config.objects.filter(projects=p), to_field_name='configName')

        self.fields['queue'] = queue