# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..ninjas.models import Ninja


class Avatar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="avatars/")
    users_using_avatar = models.ForeignKey(Ninja, related_name='avatar', null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
