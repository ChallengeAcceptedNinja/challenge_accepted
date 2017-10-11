# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from ..challenges.models import Challenge

class ChallengeSession(models.Model):
    number = models.IntegerField(default=None, null=True)
    challenge = models.ForeignKey(Challenge, related_name='sessions', default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def winners(self):
        bouts = self.bouts.all()
        winners = []
        for bout in bouts:
            winners.append(bout.winner)
        return winners    

    @property
    def losers(self):
        bouts = self.bouts.all()
        losers = []
        for bout in bouts:
            losers.append(bout.loser)
        return losers   

    @property
    def participants(self):
        bouts = self.bouts.all()
        results = []
        for bout in bouts:
            participants = bout.participants.all()
            for participant in participants:
                results.append(participant)
        return results    
        # return self.bouts.prefetch_related('challenge_session').values()
        # return self.bouts.prefetch_related().iterator()

