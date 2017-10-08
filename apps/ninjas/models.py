# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib import messages

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
                data['username'],
                data['email'],
                data['password'],
            )
            new_ninja.first_name = data['first_name']
            new_ninja.last_name = data['last_name']
            new_ninja.save()
            return new_ninja
        else:
            # for tag in errors:
                # messages.error(request, errors[tag])
            return None
            


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
