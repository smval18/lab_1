from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from polls.models import NewUser


class RegisterUser(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ['username', 'password1', 'password2', 'photo_avatar']

