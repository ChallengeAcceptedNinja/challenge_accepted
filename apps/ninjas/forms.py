from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Ninja

class NinjaRegistrationForm(UserCreationForm):
    email = forms.EmailField()

class NinjaLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
