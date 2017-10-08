# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Ninja(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def challenges_won(self):
        return 0

    @property
    def challenges_lost(self):
        return 0
