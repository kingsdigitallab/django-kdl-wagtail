# Generated by Django 2.1.5 on 2019-01-31 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kdl_wagtail_people', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='summary',
            new_name='introduction',
        ),
    ]
