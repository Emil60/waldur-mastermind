# Generated by Django 2.2.13 on 2020-12-29 11:51

from django.db import migrations

import waldur_core.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('openstack_tenant', '0014_cidr_ipv6'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internalip',
            name='ip4_address',
        ),
        migrations.RemoveField(
            model_name='internalip',
            name='ip6_address',
        ),
        migrations.AddField(
            model_name='internalip',
            name='fixed_ips',
            field=waldur_core.core.fields.JSONField(
                default=list,
                help_text='A list of tuples (ip_address, subnet_id), where ip_address can be both IPv4 and IPv6 and subnet_id is a backend id of the subnet',
            ),
        ),
    ]
