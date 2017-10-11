# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import View

class ChallengeView(View):
    def get(self, request):
        return render(request, 'challenges/signup.html')

    def post(self, request):
        pass