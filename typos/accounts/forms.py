#encoding=utf8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(forms.Form):
    username=forms.CharField(label=_(u"username"),max_length=30,widget=forms.TextInput(attrs={'size': 20,'placeholder':'用户名'}))
    password=forms.CharField(label=_(u"password"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,'placeholder':'密码'}))
