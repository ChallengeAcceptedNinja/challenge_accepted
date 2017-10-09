# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Dojo
from ..ninjas.models import Ninja

# Create your tests here.
class DojoModelTest(TestCase):
  def test_that_dojo_can_be_created_and_saved(self):
    dojo = Dojo.objects.create(name='dojo')
    self.assertTrue(dojo)
  
  def test_that_ninjas_can_join_a_dojo(self):
    ninja1 = Ninja.objects.create_user('bob', 'bobby@ross.com', 'password')
    ninja2 = Ninja.objects.create_user('jorge', 'jorge@ross.com', 'password')

    dojo = Dojo.objects.create(name='dojo')
    dojo.members.add(ninja1, ninja2)
    dojo.save()
    self.assertEqual(dojo.members.count(), 2)
    self.assertIn(ninja1, dojo.members.all())
    self.assertIn(ninja2, dojo.members.all())
  
  def test_that_ninjas_can_become_senseis_of_a_dojo(self):
    ninja1 = Ninja.objects.create_user('bob', 'bobby@ross.com', 'password')
    dojo = Dojo.objects.create(name='dojo')
    dojo.senseis.add(ninja1)
    dojo.save()
    self.assertEqual(dojo.senseis.count(), 1)
    self.assertIn(ninja1, dojo.senseis.all())