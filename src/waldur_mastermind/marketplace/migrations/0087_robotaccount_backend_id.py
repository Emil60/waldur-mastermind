# Generated by Django 3.2.18 on 2023-05-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('marketplace', '0086_backend_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='robotaccount',
            name='backend_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
