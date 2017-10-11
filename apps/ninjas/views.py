# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import NinjaRegistrationForm, NinjaLoginForm
from .models import Ninja

class Index(View):
    def get(self, request):
        return render(request, 'ninjas/index.html')

class Register(View):
    def get(self, request):
        context = {
            'registration_form': NinjaRegistrationForm()
        }
        return render(request, 'ninjas/register.html', context)
  
    def post(self, request):
        errors = {}
        form = NinjaRegistrationForm(request.POST)
        if (form.is_valid()):
            result = Ninja.objects.validate_registration(form.cleaned_data)
            if (type(result) is not type({})):
                login(request, result)
                return redirect(reverse('ninjas:dashboard'))
            else:
                errors.update(result)
        errors.update(form.errors)
        add_errors(request, errors)
        return redirect(reverse('ninjas:register'))

class Login(View):
    def get(self, request):
        context = {
            'login_form': NinjaLoginForm()
        }
        return render(request, 'ninjas/login.html', context)
  
    def post(self, request):
        errors = {}
        form = NinjaLoginForm(request.POST)
        if (form.is_valid()):
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect(reverse('ninjas:dashboard'))
            else:
                errors.update({
                    'invalid': 'Username and/or password is invalid.'
                })
        errors.update(form.errors)
        add_errors(request, errors)
        return redirect(reverse('ninjas:login'))

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'ninjas/dashboard.html')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))

def add_errors(request, errors):
    for tag in errors:
        messages.error(request, errors[tag])