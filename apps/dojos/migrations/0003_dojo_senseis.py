# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninjas', '0002_auto_20171008_1136'),
        ('dojos', '0002_dojo_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='dojo',
            name='senseis',
            field=models.ManyToManyField(related_name='sensei_of_dojos', to='ninjas.Ninja'),
        ),
    ]
