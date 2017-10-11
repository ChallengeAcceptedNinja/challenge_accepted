from django.forms import ModelForm
from django import forms
from .models import Ninja

class NinjaRegistrationForm(ModelForm):
    
    class Meta:
        model = Ninja
        fields = ('username', 'email')
        help_texts = {
            'username': ''
        }
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_password(self):
        password1 = self.data.get('password')
        password2 = self.data.get('password_confirm')
        if str(password1) != str(password2):
            raise forms.ValidationError('Passwords must match.')

class NinjaLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)