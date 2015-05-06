# encoding: utf-8

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': '用户名不能为空'}, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'required': '密码不能为空'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                self.add_error('password', '请输入正确的用户名、密码')

        return self.cleaned_data

class RegisterForm(forms.Form):
    id = forms.CharField(error_messages={'required': '学号/工号不能为空', 'max_length':'最多是 11 个字'}, max_length = 11)
    name = forms.CharField(error_messages={'required': '姓名不能为空', 'max_length': '最多是 10 个字'}, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, error_messages = {'required': '密码不能为空', 'min_length':'至少是 6 个字符', 'max_length':'最多是 16 个字符'}, min_length = 6, max_length = 16)
    confirm_password = forms.CharField(widget=forms.PasswordInput, error_messages = {'required': '确认密码不能为空', 'min_length':'至少是 6 个字符', 'max_length':'最多是 16 个字符'}, max_length = 16)
    title = forms.CharField(max_length=20, required=False)

    TYPE_CHOICES = (
        ('student', '学生',),
        ('teacher', '教师',),
        ('manager', '教务员',),
    )
    type = forms.ChoiceField(widget=forms.Select, choices=TYPE_CHOICES)

    def clean_id(self):
        id = self.cleaned_data['id']
        exists = User.objects.filter(username = id).count() > 0
        if exists:
            self.add_error('id', '该学号/工号已被使用，请重新输入')
        return id

    def clean(self):
        if ('confirm_password' in self.cleaned_data) and ('password' in self.cleaned_data):
            if (self.cleaned_data['confirm_password'] != self.cleaned_data['password']):
                self._errors["confirm_password"] = ErrorList(['密码和确认密码不一致'])
                del self.cleaned_data['password']
                del self.cleaned_data['confirm_password']

        return self.cleaned_data
