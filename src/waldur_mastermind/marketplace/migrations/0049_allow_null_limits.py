# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-20 20:34
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0048_resource_mandatory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='limits',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
