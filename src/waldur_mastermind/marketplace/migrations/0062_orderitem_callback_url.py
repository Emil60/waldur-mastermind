# Generated by Django 2.2.25 on 2021-12-28 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0061_order_item_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='callback_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]