# Generated by Django 2.2.13 on 2021-03-17 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0047_componentusage_backend_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offeringcomponent',
            name='product_code',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='product_code',
        ),
    ]
