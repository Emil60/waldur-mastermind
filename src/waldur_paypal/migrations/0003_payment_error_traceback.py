# Generated by Django 2.2.13 on 2020-10-07 11:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('waldur_paypal', '0002_immutable_default_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='error_traceback',
            field=models.TextField(blank=True),
        ),
    ]
