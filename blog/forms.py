from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # default is required=True

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','is_staff','is_superuser']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeForm (forms.Form) :
    old_password = forms.CharField(widget=forms.PasswordInput) 
    new_password1 = forms.CharField(widget=forms.PasswordInput) 
    new_password2 = forms.CharField(widget=forms.PasswordInput) 
