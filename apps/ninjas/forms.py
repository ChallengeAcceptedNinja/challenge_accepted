from django.contrib.auth.forms import UserCreationForm
from django import forms

class NinjaRegistrationForm(UserCreationForm):
  email = forms.EmailField()