# Generated by Django 2.2.10 on 2020-10-16 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kdl_wagtail_core', '0020_contactusfield_clean_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactusfield',
            name='clean_name',
        ),
    ]