# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from copy import copy
import simplejson

from .forms import ChallengeInitiateForm
from .models import Challenge
from ..ninjas.models import Ninja
from ..challenge_sessions.models import ChallengeSession
from ..session_bouts.models import SessionBout

class ChallengeIndex(View):
    def get(self, request, challenge_id):
        context = {
            'challenge_id': challenge_id,
        }
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            context['data'] = simplejson.dumps(generate_challenge_data(challenge_id))
            return render(request, 'challenges/challenge.html', context)
        except:
            return redirect(reverse('ninjas:dashboard'))
    
    def post(self, request):
        pass

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
                new_session = ChallengeSession.objects.create(number=1)
                new_session.challenge=result
                new_session.save()
                new_bout = SessionBout.objects.create()
                new_bout.challenge_session=new_session
                new_bout.participants.add(current_user)
                new_bout.save()
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


def generate_challenge_data(challenge_id):
    # Get the challenge
    try:
        challenge = Challenge.objects.get(id=challenge_id)
        sessions = ChallengeSession.objects.filter(challenge=challenge).order_by('number')
        data = {
            'teams': [],
            'results': []
        }
    except:
        data = {}
    
    # Format session bouts data
    try:
        for session in sessions.all():
            session_results = []
            for bout in session.bouts.all():
                participants = []
                bout_scores = []
                for participant in bout.participants.all():
                    participants.append(participant.username)
                    if bout.winner == participant:
                        bout_scores.append(1)
                    elif bout.loser == participant:
                        bout_scores.append(0)
                    else:
                        bout_scores.append(None)
                session_results.append(bout_scores)
                if session.number == 1:
                    data['teams'].append(participants)
            data['results'].append(session_results)
    except:
        pass
    return data

def add_errors(request, errors):
    for tag in errors:
        messages.error(request, errors[tag])
