# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-11-29 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181124_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='null', max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
