# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from ..ninjas.models import Ninja

import datetime


class ChallengeManager(models.Manager):
    def create_challenge(self, data):
        ninja = Ninja.objects.get(id=data['user_id'])
        new_challenge = self.create(
            name=data['challenge_name'],
            description=data['description'],
            start_date=data['start_date'],
            signup_end_date=data['signup_end_date'],
            planned_by=ninja,
        )
        return new_challenge


class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(default=None, null=True)
    signup_end_date = models.DateField(default=None, null=True)
    planned_by = models.ForeignKey(Ninja, related_name="challenges_planned", default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChallengeManager()

    @property
    def winner(self):
        sessions = self.sessions.all()
        return sessions.last()

    @property
    def losers(self):
        losers = []
        sessions = self.sessions.all()
        for session in sessions:
            bouts = session.bouts.all()
            for bout in bouts:
                losers.append(bout.loser)
        return losers   

    @property
    def participants(self):
        results = []
        sessions = self.sessions.all()
        for session in sessions:
            bouts = session.bouts.all()
            for bout in bouts:
                participants = bout.participants.all()
                for participant in participants:
                    results.append(participant)
        return results