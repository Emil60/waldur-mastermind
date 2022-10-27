# Generated by Django 3.2.15 on 2022-10-11 13:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0073_update_internal_name_validator'),
        ('invoices', '0061_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='resource',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='invoice_items',
                to='marketplace.resource',
            ),
        ),
    ]