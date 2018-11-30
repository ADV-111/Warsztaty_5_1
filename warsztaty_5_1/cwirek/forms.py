from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4})
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'Email',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
        }
