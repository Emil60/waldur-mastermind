# Generated by Django 2.2.19 on 2021-04-02 10:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('logging', '0008_drop_sec_group_rules_pulling_events'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PushHook',
        ),
    ]
