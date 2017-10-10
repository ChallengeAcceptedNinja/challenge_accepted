# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
  return render(request, 'ninjas/index.html')

def register(request):
  return render(request, 'ninjas/register.html')

def login(request):
  return render(request, 'ninjas/login.html')

def dashboard(request):
  return render(request, 'ninjas/dashboard.html')
