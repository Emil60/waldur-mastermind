# Generated by Django 1.11.4 on 2018-03-02 11:41
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('waldur_jira', '0013_extend_jira_issue_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='updated_username',
            new_name='creator_username',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='assignee',
        ),
        migrations.AddField(
            model_name='issue',
            name='assignee_email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='issue',
            name='assignee_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='issue',
            name='assignee_username',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='issue',
            name='creator_email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter_email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter_username',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
