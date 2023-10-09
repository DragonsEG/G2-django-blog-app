from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm

from .models import Comment

class unUniqueCharField (forms.CharField):
    def validate(self, value):
        pass

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                            widget=forms.Textarea)
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','body']

class SearchForm(forms.Form):
    query = forms.CharField()


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first = unUniqueCharField(max_length=50)
    last = unUniqueCharField(max_length=50)

    class Meta:
        model = User
        fields = ['first', 'last', 'username',  'email', 'password1',
                'password2', 'is_staff', 'is_superuser']
