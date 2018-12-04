from django import forms
from .models import Tweet, User, Profile, Comments, Messages
from django.contrib.auth.forms import UserCreationForm


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        labels = {
            'content': 'Zawartość komentarza',
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content']
        labels = {
            'content': 'Zawartość wiadomości',
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        labels = {
            'email': 'Email',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
