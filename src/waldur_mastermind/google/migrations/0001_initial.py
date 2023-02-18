# Generated by Django 2.2.13 on 2020-11-13 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('marketplace', '0033_mandatory_offering_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCredentials',
            options={
                'verbose_name': 'Google credentials',
                'verbose_name_plural': 'Google credentials',
            },
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('client_id', models.CharField(max_length=255)),
                ('project_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('calendar_token', models.CharField(blank=True, max_length=255)),
                (
                    'calendar_refresh_token',
                    models.CharField(blank=True, max_length=255),
                ),
                (
                    'service_provider',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='marketplace.ServiceProvider',
                    ),
                ),
            ],
        ),
    ]
