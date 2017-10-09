# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..ninjas.models import Ninja
from ..challenge_sessions.models import ChallengeSession

class SessionBout(models.Model):
    participants = models.ManyToManyField(Ninja, related_name='participated_session_bouts')
    challenge_session = models.ForeignKey(ChallengeSession, related_name='bouts', default=None, null=True)
    winner = models.ForeignKey(Ninja, related_name='session_bout_wins', default=None, null=True)
    loser = models.ForeignKey(Ninja, related_name='session_bout_losses', default=None, null=True)

    @property
    def is_full(self):
        return self.participants.count() >= 2