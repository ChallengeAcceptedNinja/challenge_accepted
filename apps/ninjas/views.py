# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import View
from django.contrib.auth import authenticate

from .forms import NinjaRegistrationForm, NinjaLoginForm
from .models import Ninja

def index(request):
    return render(request, 'ninjas/index.html')

class RegisterView(View):
    def get(self, request):
        context = {
            'registration_form': NinjaRegistrationForm()
        }
        return render(request, 'ninjas/register.html', context)
  
    def post(self, request):
        form = NinjaRegistrationForm(request.POST)
        if (form.is_valid()):
            result = Ninja.objects.validate_registration(form.cleaned_data)
            if (type(result) is not type({})):
                return redirect(reverse('ninjas:dashboard'))
        return redirect(reverse('ninjas:register'))

class LoginView(View):
    def get(self, request):
        context = {
            'login_form': NinjaLoginForm()
        }
        return render(request, 'ninjas/login.html', context)
  
    def post(self, request):
        form = NinjaLoginForm(request.POST)
        if (form.is_valid()):
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                return redirect(reverse('ninjas:dashboard'))
        return redirect(reverse('ninjas:login'))

def dashboard(request):
    return render(request, 'ninjas/dashboard.html')
