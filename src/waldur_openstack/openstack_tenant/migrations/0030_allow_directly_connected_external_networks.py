# Generated by Django 3.2.14 on 2022-08-14 20:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('openstack_tenant', '0029_flavor_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='connect_directly_to_external_network',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instance',
            name='directly_connected_ips',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
