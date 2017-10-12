# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Challenge
from ..ninjas.models import Ninja
from ..challenge_sessions.models import ChallengeSession
from ..session_bouts.models import SessionBout
from copy import copy
from django.contrib import messages


from .forms import ChallengeInitiateForm

class InitiateChallenge(View):
    def get(self, request):
        context = {
            'init_challenge_form': ChallengeInitiateForm(),
        }
        return render(request, 'challenges/new.html', context)

    def post(self, request):
        errors = {}
        form = ChallengeInitiateForm(request.POST)
        if (form.is_valid()):
            data = copy(form.cleaned_data)
            data['user_id'] = self.request.user.id
            result = Challenge.objects.create_challenge(data)
            if (type(result) is not type({})):
                current_user = Ninja.objects.get(id=self.request.user.id)
                new_session = ChallengeSession.objects.create()
                new_session.challenge=result
                new_session.save()
                new_bout = SessionBout.objects.create()
                new_bout.challenge_session=new_session
                new_bout.participants.add(current_user)
                new_bout.save()
                print request.POST
                return redirect(reverse('ninjas:dashboard'))
            else:
                errors.update(result)
        errors.update(form.errors)
        add_errors(request, errors)
        return redirect(reverse('challenges:new'))


class JoinChallenge(View):
    def get(self, request):
        return render(request, 'challenges/join_challenge.html')

    def post(self, request):
        return redirect(reverse('ninjas:dashboard'))

def add_errors(request, errors):
    for tag in errors:
        messages.error(request, errors[tag])
