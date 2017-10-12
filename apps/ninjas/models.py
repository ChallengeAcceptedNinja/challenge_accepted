# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, UserManager

class NinjaManager(UserManager):
    def validate_registration(self, data):
        emails = self.filter(email=data['email'])
        usernames = self.filter(username=data['username'])
        errors = {}
        if len(emails) > 0:
            errors['email'] = 'Email already exists.'
        if len(usernames) > 0:
            errors['username'] = 'Username already exists.'
        if not errors:
            new_ninja = self.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
            return new_ninja
        else:
            return errors

class Ninja(User):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = NinjaManager()
    
    @property
    def challenges_won(self):
        return 0

    @property
    def challenges_lost(self):
        return 0