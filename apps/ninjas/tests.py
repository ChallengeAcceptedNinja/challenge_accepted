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

    def test_that_username_is_unique(self):
        bobby = Ninja.objects.validate_registration({
            'username': 'bobby',
            'email': 'bobby@ross.com',
            'password': 'password',
            'password_confirm': 'password',
        })

        jorge = Ninja.objects.validate_registration({
            'username': 'bobby',
            'email': 'rossy@ross.com',
            'password': 'password',
            'password_confirm': 'password',
        })

        self.assertEqual(Ninja.objects.count(), 1)

    def test_that_email_is_unique(self):
        bobby = Ninja.objects.validate_registration({
            'username': 'bobby',
            'email': 'bobby@ross.com',
            'password': 'password',
            'password_confirm': 'password',
        })

        jorge = Ninja.objects.validate_registration({
            'username': 'jorgy',
            'email': 'bobby@ross.com',
            'password': 'password',
            'password_confirm': 'password',
        })

        self.assertEqual(Ninja.objects.count(), 1)
