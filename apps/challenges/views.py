# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import View

from .forms import ChallengeInitiateForm

class InitiateChallenge(View):
    def get(self, request):
        context = {
            'init_challenge_form': ChallengeInitiateForm()
        }
        return render(request, 'challenges/new.html', context)

    def post(self, request):
        pass