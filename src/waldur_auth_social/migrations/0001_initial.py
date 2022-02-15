# Generated by Django 2.2.24 on 2021-08-09 12:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthToken',
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
                ('provider', models.CharField(max_length=32)),
                ('access_token', models.TextField()),
                ('refresh_token', models.TextField()),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='auth_profile',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'unique_together': {('user', 'provider')},
            },
        ),
    ]
