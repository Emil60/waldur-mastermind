# Generated by Django 2.2.13 on 2020-08-06 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('support', '0007_extended_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='offering',
            name='backend_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
