# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from copy import copy
import simplejson, datetime

from .forms import ChallengeInitiateForm
from .models import Challenge
from ..ninjas.models import Ninja
from ..challenge_sessions.models import ChallengeSession
from ..session_bouts.models import SessionBout

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
                generate_bouts(new_session)
                return redirect(reverse('ninjas:dashboard'))
            else:
                errors.update(result)
        errors.update(form.errors)
        add_errors(request, errors)
        return redirect(reverse('challenges:new'))

class JoinChallenge(View):
    def get(self, request, challenge_id):
        context = {
            'challenge_id': challenge_id,
        }
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            context['data'] = simplejson.dumps(generate_challenge_data(challenge_id))
            return render(request, 'challenges/challenge.html', context)
        except:
            pass
        return redirect(reverse('ninjas:dashboard'))
    
    def post(self, request, challenge_id):
        # Join challenge
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            print "challenge:", challenge
            ninja = Ninja.objects.get(id=self.request.user.id)
            print "ninja:", ninja
            add_ninja_to_challenge(ninja, challenge)
        except:
            pass
        return redirect(reverse('challenges:join', kwargs={ 'challenge_id': challenge_id }))

class Bouts(View):
    def get(self, request):
        context = {}
        bouts_data = []
        try:
            ninja = Ninja.objects.get(id=self.request.user.id)
            all_session_bouts = SessionBout.objects.all()
            for bout in all_session_bouts:
                if ninja in bout.participants.all():
                    temp = get_bout_data(ninja, bout)
                    if bout_is_active(bout):
                        bouts_data.append(temp)
        except:
            pass
        context['bouts'] = bouts_data
        return render(request, 'challenges/bouts.html', context)
    
    def post(self, request):
        pass

class DetermineResult(View):
    def get(self, request, challenge_id, bout_id, won):
        bout = SessionBout.objects.get(id=bout_id)
        ninja = Ninja.objects.get(id=self.request.user.id)
        for participant in bout.participants.all():
            if participant != ninja:
                opponent = participant
        if won:
            bout.winner = ninja
            bout.loser = opponent
        else:
            bout.winner = opponent
            bout.loser = ninja
        return redirect(reverse('challenges:join'), kwargs={ 'challenge_id': challenge_id })
    
    def post(self, request):
        pass

def generate_bouts(session):
    num_bouts = SessionBout.objects.filter(challenge_session=session).count()
    first_bout = None
    while (num_bouts % 4 != 0):
        temp = SessionBout.objects.create(challenge_session=session)
        if first_bout is None:
            first_bout = temp
        num_bouts = SessionBout.objects.filter(challenge_session=session).count()
    return first_bout

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
    # TODO: FIX ME
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
                if len(bout_scores) < 2:
                    bout_scores.append(None)
                session_results.append(bout_scores)
                if session.number == 1:
                    if not bout.is_full:
                        participants.append(None)
                        bout_scores.append(None)
                    if len(participants) < 2:
                        participants.append(None)
                    data['teams'].append(participants)
            data['results'].append(session_results)
    except:
        pass
    return data

def add_ninja_to_challenge(ninja, challenge):
    # Ninja can only join the first session
    try:
        first_session = ChallengeSession.objects.get(challenge=challenge, number=1)
        all_bouts = SessionBout.objects.filter(challenge_session=first_session)
        for bout in all_bouts:
            if not bout.is_full:
                bout.participants.add(ninja)
                bout.save()
                break
        next_open_bout = generate_bouts()
        next_open_bout.participants.add(ninja)
        next_open_bout.save()
    except:
        pass

def bout_is_active(bout):
    now = datetime.datetime.today()
    session1 = bout.challenge_session
    challenge1 = session1.challenge
    return now > challenge1.start_date

def get_bout_data(ninja, bout):
    data = {}
    session1 = bout.challenge_session
    challenge1 = session1.challenge
    data['challenge_name'] = challenge1.name
    data['bout_id'] = bout.id
    data['challenge_id'] = challenge1.id
    for participant in bout.participants.all():
        if ninja != participant:
            data['opponent'] = participant.username
    return data

def add_errors(request, errors):
    for tag in errors:
        messages.error(request, errors[tag])