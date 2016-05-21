from django import forms


class LoginForm(forms.Form):
	userName = forms.CharField(max_length=10)
	passWord = forms.CharField(max_length=10, widget=forms.PasswordInput)
