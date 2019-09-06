# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-12 06:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='salary',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.PositiveIntegerField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
