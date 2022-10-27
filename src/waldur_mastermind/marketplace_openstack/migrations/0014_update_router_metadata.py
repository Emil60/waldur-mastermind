# Generated by Django 3.2.14 on 2022-09-27 09:27

from django.db import migrations

from waldur_mastermind.marketplace_openstack.handlers import (
    synchronize_router_backend_metadata,
)


def update_metadata(apps, schema_editor):
    Router = apps.get_model('openstack', 'Router')

    for router in Router.objects.all():
        synchronize_router_backend_metadata(None, router, True)


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace_openstack', '0013_rename_offering_type'),
    ]

    operations = [
        migrations.RunPython(update_metadata),
    ]