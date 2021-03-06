# Generated by Django 2.1.7 on 2019-03-04 13:18

from django.db import migrations
import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('kdl_wagtail_core', '0006_alignmentchoiceblock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streampage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading_block', wagtail.core.blocks.StructBlock([('heading_text', wagtail.core.blocks.CharBlock(classname='title', required=True)), ('size', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5')]))])), ('richtext_block', wagtail.core.blocks.RichTextBlock(icon='pilcrow', template='kdl_wagtail_core/blocks/richtext_block.html')), ('document_block', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('transcription', wagtail.core.blocks.RichTextBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=True))])), ('gallery_block', wagtail.core.blocks.StructBlock([('images_block', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('transcription', wagtail.core.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Select block alignment'), ('left', 'Left'), ('right', 'Right'), ('center', 'Centre'), ('full-width', 'Full width')]))])))])), ('image_block', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('transcription', wagtail.core.blocks.RichTextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('', 'Select block alignment'), ('left', 'Left'), ('right', 'Right'), ('center', 'Centre'), ('full-width', 'Full width')]))])), ('link_block', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock(required=False)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('label', wagtail.core.blocks.CharBlock())])), ('embed_block', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('transcription', wagtail.core.blocks.RichTextBlock(required=False)), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL', icon='media'))])), ('table_block', wagtail.core.blocks.StructBlock([('caption', wagtail.core.blocks.CharBlock(required=False)), ('attribution', wagtail.core.blocks.CharBlock(required=False)), ('description', wagtail.core.blocks.RichTextBlock(required=False)), ('transcription', wagtail.core.blocks.RichTextBlock(required=False)), ('table', wagtail.contrib.table_block.blocks.TableBlock(required=True))]))], blank=True, verbose_name='Page body'),
        ),
    ]
