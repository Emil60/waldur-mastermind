# Generated by Django 3.2.14 on 2022-10-07 19:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('structure', '0034_notification_notificationtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='default_tax_percent',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=4,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(200),
                ],
            ),
        ),
    ]
