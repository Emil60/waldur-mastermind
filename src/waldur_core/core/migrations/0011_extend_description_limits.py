# Generated by Django 2.2.13 on 2020-09-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_changeemailrequest_uuid_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(
                blank=True, max_length=2000, verbose_name='description'
            ),
        ),
    ]
