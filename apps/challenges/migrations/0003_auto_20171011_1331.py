# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_auto_20171009_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='signup_end_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='challenge',
            name='start_date',
            field=models.DateTimeField(default=None),
        ),
    ]
