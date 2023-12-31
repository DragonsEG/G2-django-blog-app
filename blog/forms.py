from typing import Any
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, BaseUserCreationForm
from django.contrib.auth import password_validation
from .models import *


class unUniqueCharField (forms.CharField):
    def validate(self, value):
        pass


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # default is required=True
    first = unUniqueCharField(max_length=50)
    last = unUniqueCharField(max_length=50)

    class Meta:
        model = User
        fields = ['first', 'last', 'username',  'email', 'password1',
                  'password2', 'is_superuser']


class CompanyRegistration (UserCreationForm):
    email = forms.EmailField(label='Company Mail')
    username = forms.CharField(widget=forms.TextInput(),  label='Company Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeForm (forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)


class EditUserProfileForm(UserChangeForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
