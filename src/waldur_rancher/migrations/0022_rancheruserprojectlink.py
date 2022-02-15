# Generated by Django 2.2.10 on 2020-06-11 09:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waldur_rancher', '0021_rancher_user_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='RancherUserProjectLink',
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
                ('backend_id', models.CharField(blank=True, max_length=255)),
                ('role', models.CharField(max_length=255)),
                (
                    'project',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='waldur_rancher.Project',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='waldur_rancher.RancherUser',
                    ),
                ),
            ],
            options={
                'unique_together': {('user', 'project', 'role')},
            },
        ),
    ]
