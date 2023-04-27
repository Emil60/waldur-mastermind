# Generated by Django 3.2.18 on 2023-04-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('marketplace', '0084_resource_end_date_requested_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='robotaccount',
            name='backend_metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='offeringuser',
            name='backend_metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]