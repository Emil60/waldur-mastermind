# Generated by Django 2.2.26 on 2022-01-26 11:14

import django.db.models.deletion
from django.db import migrations, models

import waldur_core.core.fields
import waldur_core.core.models
import waldur_core.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('structure', '0026_project_managers'),
        ('openstack_tenant', '0022_securitygrouprule_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerGroup',
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
                (
                    'name',
                    models.CharField(
                        max_length=150,
                        validators=[waldur_core.core.validators.validate_name],
                        verbose_name='name',
                    ),
                ),
                ('uuid', waldur_core.core.fields.UUIDField()),
                ('backend_id', models.CharField(db_index=True, max_length=255)),
                (
                    'policy',
                    models.CharField(
                        blank=True, choices=[('Affinity', 'Affinity')], max_length=40
                    ),
                ),
                (
                    'settings',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to='structure.ServiceSettings',
                    ),
                ),
            ],
            options={
                'unique_together': {('settings', 'backend_id')},
            },
            bases=(waldur_core.core.models.BackendModelMixin, models.Model),
        ),
    ]
