# Generated by Django 4.0.4 on 2022-04-27 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtrackerapp', '0013_userprofile_bio_userprofile_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurerequest',
            name='msg',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
