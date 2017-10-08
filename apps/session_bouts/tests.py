# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import SessionBout
from ..ninjas.models import Ninja

class SessionBoutsModelTest(TestCase):
    def test_that_session_bout_can_be_created_and_saved(self):
        session_bout = SessionBout.objects.create()
        self.assertTrue(session_bout)

    def test_add_ninjas_to_session_bout(self):
        ninja1 = Ninja.objects.create_user('bob', 'bobby@ross.com', 'password')
        ninja2 = Ninja.objects.create_user('jorge', 'jorge@ross.com', 'password')
        session_bout = SessionBout.objects.create()        
        session_bout.participants.add(ninja1, ninja2)
        self.assertIn(ninja1, session_bout.participants.all())
        self.assertIn(ninja2, session_bout.participants.all())

    def test_if_bout_is_full(self):
        ninja1 = Ninja.objects.create_user('bob', 'bobby@ross.com', 'password')
        ninja2 = Ninja.objects.create_user('jorge', 'jorge@ross.com', 'password')
        session_bout = SessionBout.objects.create()
        self.assertFalse(session_bout.is_full)      
        session_bout.participants.add(ninja1, ninja2)
        self.assertTrue(session_bout.is_full)