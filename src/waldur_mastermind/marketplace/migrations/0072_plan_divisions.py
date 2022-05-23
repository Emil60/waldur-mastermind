# Generated by Django 3.2.12 on 2022-04-18 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0028_project_is_industry'),
        ('marketplace', '0071_offeringuser_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='divisions',
            field=models.ManyToManyField(
                blank=True, related_name='plans', to='structure.Division'
            ),
        ),
    ]