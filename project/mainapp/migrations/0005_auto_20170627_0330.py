# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 03:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20170619_1813'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dailyrate',
            unique_together=set([]),
        ),
    ]
