# Generated by Django 2.2.1 on 2019-05-16 10:26

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kdl_wagtail_zotero', '0007_bibliography_citation_short'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliography',
            name='bib',
            field=wagtail.core.fields.RichTextField(verbose_name='bibliography entry'),
        ),
        migrations.AlterField(
            model_name='bibliography',
            name='citation',
            field=wagtail.core.fields.RichTextField(verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='bibliography',
            name='citation_short',
            field=wagtail.core.fields.RichTextField(null=True, verbose_name='shortnote'),
        ),
    ]