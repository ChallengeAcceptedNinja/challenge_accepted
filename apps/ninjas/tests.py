# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ninja

# Test that we can create and save user
class UsersTest(TestCase):
    def test_that_user_can_be_created_and_saved(self):
        ninjas = Ninja.objects.create_user('bob', 'bobby@ross.com', 'password')
        all_ninjas = Ninja.objects.all()
        self.assertIn(ninjas, all_ninjas)