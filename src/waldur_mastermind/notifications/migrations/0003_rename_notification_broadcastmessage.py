# Generated by Django 3.2.14 on 2022-09-16 08:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0002_json_field'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notification',
            new_name='BroadcastMessage',
        ),
    ]
