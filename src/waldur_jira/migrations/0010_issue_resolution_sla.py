# Generated by Django 1.11.7 on 2018-02-13 21:26
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('waldur_jira', '0009_drop_old_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='resolution_sla',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
