# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..ninjas.models import Ninja

class Dojo(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Ninja, related_name='member_of_dojos')
    senseis = models.ManyToManyField(Ninja, related_name='sensei_of_dojos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)