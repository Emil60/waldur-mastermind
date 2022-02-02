# Generated by Django 3.2 on 2022-02-01 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0026_project_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpermission',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='projectpermission',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, null=True),
        ),
    ]