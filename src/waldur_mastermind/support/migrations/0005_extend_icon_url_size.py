# Generated by Django 2.2.10 on 2020-04-05 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('support', '0004_templateconfirmationcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priority',
            name='icon_url',
            field=models.URLField(blank=True, max_length=500, verbose_name='icon url'),
        ),
    ]
