# Generated by Django 2.2.10 on 2020-04-23 13:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('waldur_slurm', '0007_fill_backend_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='cpu_limit',
            field=models.BigIntegerField(default=16000),
        ),
        migrations.AlterField(
            model_name='allocation',
            name='deposit_limit',
            field=models.DecimalField(decimal_places=0, default=200, max_digits=6),
        ),
        migrations.AlterField(
            model_name='allocation',
            name='gpu_limit',
            field=models.BigIntegerField(default=400),
        ),
        migrations.AlterField(
            model_name='allocation',
            name='ram_limit',
            field=models.BigIntegerField(default=100000),
        ),
    ]
