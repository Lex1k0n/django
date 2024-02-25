from django.contrib.auth.models import User
from django import forms


class RegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']


class LoginForm(forms.Form):

    username = forms.CharField(label='UserName')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class ChangePassForm(forms.Form):

    old_pass = forms.CharField(label='Old password', widget=forms.PasswordInput)
    new_pass = forms.CharField(label='New password', widget=forms.PasswordInput)
