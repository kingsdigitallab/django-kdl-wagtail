# Generated by Django 2.2.10 on 2020-12-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kdl_wagtail_zotero', '0008_add_verbose_name_to_bibliography_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliography',
            name='item_type',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
