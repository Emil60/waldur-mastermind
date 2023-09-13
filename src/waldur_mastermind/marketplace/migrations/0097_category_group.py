# Generated by Django 3.2.18 on 2023-09-07 13:18

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import upload_validator
from django.db import migrations, models

import waldur_core.core.fields


class Migration(migrations.Migration):
    dependencies = [
        ('marketplace', '0096_translations'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGroup',
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
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                ('uuid', waldur_core.core.fields.UUIDField()),
                ('title', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255, null=True)),
                ('title_et', models.CharField(max_length=255, null=True)),
                ('title_lt', models.CharField(max_length=255, null=True)),
                ('title_lv', models.CharField(max_length=255, null=True)),
                ('title_ru', models.CharField(max_length=255, null=True)),
                ('title_it', models.CharField(max_length=255, null=True)),
                ('title_de', models.CharField(max_length=255, null=True)),
                ('title_da', models.CharField(max_length=255, null=True)),
                ('title_sv', models.CharField(max_length=255, null=True)),
                ('title_es', models.CharField(max_length=255, null=True)),
                ('title_fr', models.CharField(max_length=255, null=True)),
                ('title_nb', models.CharField(max_length=255, null=True)),
                (
                    'icon',
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to='marketplace_category_group_icons',
                        validators=[
                            upload_validator.FileTypeValidator(
                                allowed_types=[
                                    'image/png',
                                    'image/gif',
                                    'image/jpeg',
                                    'image/svg',
                                    'image/svg+xml',
                                    'image/x-icon',
                                ]
                            )
                        ],
                    ),
                ),
                ('description', models.TextField(blank=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_et', models.TextField(blank=True, null=True)),
                ('description_lt', models.TextField(blank=True, null=True)),
                ('description_lv', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('description_it', models.TextField(blank=True, null=True)),
                ('description_de', models.TextField(blank=True, null=True)),
                ('description_da', models.TextField(blank=True, null=True)),
                ('description_sv', models.TextField(blank=True, null=True)),
                ('description_es', models.TextField(blank=True, null=True)),
                ('description_fr', models.TextField(blank=True, null=True)),
                ('description_nb', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Category group',
                'verbose_name_plural': 'Category groups',
                'ordering': ('title',),
            },
        ),
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='marketplace.categorygroup',
            ),
        ),
    ]