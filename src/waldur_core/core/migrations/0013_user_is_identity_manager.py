# Generated by Django 2.2.19 on 2021-03-29 10:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_drop_slurm_packages'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_identity_manager',
            field=models.BooleanField(
                default=False,
                help_text='Designates whether the user is allowed to manage remote user identities.',
            ),
        ),
    ]
