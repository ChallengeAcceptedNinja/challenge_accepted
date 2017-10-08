# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..ninjas.models import Ninja

class ChallengeSession(models.Model):
    number = models.IntegerField(default=None, null=True)



