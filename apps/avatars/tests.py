# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Avatar
from ..ninjas.models import Ninja

class AvatarModelTest(TestCase):
    def test_that_avatar_can_be_created_and_saved(self):
        avatar = Avatar.objects.create(name='avatar', image='avatars/avatar_img.png')
        self.assertTrue(avatar)

