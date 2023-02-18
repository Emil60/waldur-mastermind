# Generated by Django 2.2.24 on 2021-12-17 10:12

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('support', '0015_fill_attachment_mime_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesttype',
            name='fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True, default=dict
            ),
        ),
    ]
