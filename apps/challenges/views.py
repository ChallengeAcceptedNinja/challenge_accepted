# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from copy import copy
import simplejson, datetime, math

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
            context['challenge_name'] = challenge.name
            context['data'] = simplejson.dumps(generate_challenge_data(challenge_id))
            return render(request, 'challenges/challenge.html', context)
        except:
            pass
        return redirect(reverse('ninjas:dashboard'))
    
    def post(self, request, challenge_id):
        # Join challenge
        try:
            challenge = Challenge.objects.get(id=challenge_id)
            ninja = Ninja.objects.get(id=self.request.user.id)
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
                if ninja_in(bout.participants.all(), ninja):
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
    def get(self, request):
        pass
    
    def post(self, request, bout_id):
        won = request.POST.get('result')
        challenge_id = request.POST.get('challenge_id')
        try:
            ninja = Ninja.objects.get(id=self.request.user.id)
            # Update this bout
            opponent = None
            bout = SessionBout.objects.get(id=bout_id)
            for participant in bout.participants.all():
                if participant != ninja:
                    opponent = participant
            if won == 'True':
                bout.winner = ninja
                bout.loser = opponent
                move_to_next_session(ninja, bout, opponent)
            else:
                bout.winner = opponent
                bout.loser = ninja
                move_to_next_session(opponent, bout, ninja)
            bout.save()
            # Create a new bout for the next session and add the winner as a participant
        except:
            pass
        return redirect(reverse('challenges:join', kwargs={ 'challenge_id': challenge_id }))

def move_to_next_session(ninja, prev_bout, to_remove=None):
    # Ninja should be advanced to bout # prev_bout.number / 2 rounded up
    prev_bout_number = get_bout_number(prev_bout)
    next_bout_number = int(math.ceil(float(prev_bout_number) / float(2)))
    # Check if next session exists, if it doesn't create it
    prev_session = prev_bout.challenge_session
    prev_session_number = prev_session.number
    print "prev session number:", prev_session_number
    challenge = prev_session.challenge
    print "moving to different session in challenge:", challenge.name
    try:
        next_session = ChallengeSession.objects.get(number=prev_session_number + 1)
    except:
        next_session = ChallengeSession.objects.create(number=prev_session_number + 1, challenge=challenge)
    next_session.save()
    print "next session number:", next_session.number
    # If bout of next_bout_number doesn't exist, create it
    try:
        next_bout = get_bout_from_session(next_bout_number, next_session)
    except:
        next_bout = SessionBout.objects.create(challenge_session=next_session)
    # Add ninja to this bout
    print "next bout participants:", next_bout.participants.all()
    next_bout.participants.add(ninja)
    next_bout.save()
    if to_remove:
        next_bout.participants.remove(to_remove)
    print next_bout.participants.all()
    print "moved", ninja.username, "to the next session and bout"

def get_bout_number(target_bout):
    count = 0
    all_bouts = target_bout.challenge_session.bouts.all().order_by('id')
    for bout in all_bouts:
        count += 1
        if bout == target_bout:
            return count
    raise ValueError('could not find that bout')

def get_bout_from_session(bout_number, session):
    count = 0
    all_bouts = session.bouts.all().order_by('id')
    for bout in all_bouts:
        count += 1
        if count == bout_number:
            print "next bout participants:", bout.participants.all()
            return bout
    raise ValueError('could not find that bout in that session')

def ninja_in(participants, ninja):
    for participant in participants:
        if participant == ninja:
            return True
    return False

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
            'teams': None,
            'results': None
        }
    except:
        data = {}
    
    try:
        teams = []
        for session in sessions.all().order_by('number'):
            session_results = []
            for bout in session.bouts.all().order_by('id'):
                participants = []
                bout_scores = [None, None]
                for participant in bout.participants.all().order_by('id'):
                    participants.append(participant.username)
                    score = None
                    if bout.winner == participant:
                        score = 1
                    elif bout.loser == participant:
                        score = 0
 
                    if session.number == 1:
                        ninja_index = len(participants) - 1
                    else:
                        locations = get_ninja_position_in_team(teams, participant)
                        ninja_index = locations['ninja_index']
                        # bout_scores[locations['ninja_index']] = score
                    bout_scores[ninja_index] = score

                session_results.append(bout_scores)
                
                if session.number == 1:
                    while len(participants) < 2:
                        participants.append(None)
                    teams.append(participants)
            data['teams'] = teams
            data['results'] = session_results
    except:
        pass
    return data

def get_ninja_position_in_team(teams, ninja):
    for team_number in range(0, len(teams)):
        for ninja_index in range(0, len(team)):
            if team[ninja_index] == ninja.username:
                return {
                    'team_number': team_number,
                    'ninja_index': ninja_index
                }
    raise ValueError('could not find that ninja in the teams provided')

def add_ninja_to_challenge(ninja, challenge):
    # Ninja can only join the first session
    try:
        first_session = ChallengeSession.objects.get(challenge=challenge, number=1)
        all_bouts = SessionBout.objects.filter(challenge_session=first_session)
        for bout in all_bouts:
            # If not full, add ninja
            if not bout.is_full:
                opponent = bout.participants.first()
                bout.participants.add(ninja)
                bout.save()
                # check if opponent needs to be removed from next session's participants
                remove_from_next_bout(bout, opponent)
                # If still not full (ninja is the only participant), move ninja onwards
                if not bout.is_full:
                    print "moving", ninja.username, "to next session because empty"
                    move_to_next_session(ninja, bout)
                break
        next_open_bout = generate_bouts()
        next_open_bout.participants.add(ninja)
        next_open_bout.save()
        if not next_bout_number.is_full:
            print "moving", ninja.username, "to next session because empty"
            move_to_next_session(ninja, bout)
    except:
        pass

def remove_from_next_bout(bout, opponent):
    prev_bout_number = get_bout_number(bout)
    next_bout_number = int(math.ceil(float(prev_bout_number) / float(2)))
    next_open_bout.participants.remove(opponent)

def bout_is_active(bout):
    now = datetime.date.today()
    session1 = bout.challenge_session
    challenge1 = session1.challenge
    return now >= challenge1.start_date

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