# Generated by Django 4.0.3 on 2022-03-11 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtrackerapp', '0008_alter_bug_priority_alter_bug_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='priority',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low'), ('Unknown', 'Unknown')], default='Low', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bug',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected')], default='Pending', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='featurerequest',
            name='status',
            field=models.CharField(blank=True, choices=[('Unverified', 'Unverified'), ('in Talk', 'in Talk'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Unverified', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='signedAs',
            field=models.CharField(blank=True, choices=[('Developer', 'Developer'), ('Tester', 'Tester'), ('Project Manager', 'Project Manager'), ('Admin', 'Admin'), ('User', 'User')], default='User', max_length=200, null=True),
        ),
    ]