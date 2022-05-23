# Generated by Django 3.2.12 on 2022-02-04 08:28

import django.utils.timezone
import model_utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0070_alter_offeringpermission_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='offeringuser',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name='modified',
            ),
        ),
        migrations.AlterField(
            model_name='offeringuser',
            name='created',
            field=model_utils.fields.AutoCreatedField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name='created',
            ),
        ),
    ]