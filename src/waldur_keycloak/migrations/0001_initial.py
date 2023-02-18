# Generated by Django 2.2.24 on 2021-07-29 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('structure', '0024_project_oecd_fos_2007_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectGroup',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('backend_id', models.UUIDField()),
                (
                    'project',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='structure.Project',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('backend_id', models.UUIDField()),
                (
                    'customer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='structure.Customer',
                    ),
                ),
            ],
        ),
    ]
