# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import ChallengeSession
from ..ninjas.models import Ninja
from ..session_bouts.models import SessionBout

class ChallengeSessionModelTest(TestCase):
    def test_that_challenge_session_can_be_created_and_saved(self):
        challenge_session = ChallengeSession.objects.create()
        self.assertTrue(challenge_session)
