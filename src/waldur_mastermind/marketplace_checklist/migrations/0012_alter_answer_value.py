# Generated by Django 3.2 on 2022-02-01 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace_checklist', '0011_question_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='value',
            field=models.BooleanField(null=True),
        ),
    ]
