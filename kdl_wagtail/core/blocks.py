from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.blocks import (CharBlock, ChoiceBlock, ListBlock,
                                 PageChooserBlock, RichTextBlock, StreamBlock,
                                 StructBlock, URLBlock)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock as WagtailEmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class BaseCaptionAttributionBlock(StructBlock):
    """
    Base `StructBlock` to create blocks that use captions and attribution
    fields.
    """
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)


class DocumentBlock(BaseCaptionAttributionBlock):
    """
    `StructBlock` for using documents with associated caption and attribution.
    """
    document = DocumentChooserBlock(required=True)

    class Meta:
        icon = 'doc-full'
        template = 'kdl_wagtail_core/blocks/document_block.html'


class EmbedBlock(BaseCaptionAttributionBlock):
    """
    `StructBlock` for using embeds with associated caption and attribution.
    """
    embed_block = WagtailEmbedBlock(
        help_text='Insert an embed URL', icon='media')

    class Meta:
        icon = 'media'
        template = 'kdl_wagtail_core/blocks/embed_block.html'


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h5 sizes for
    headers.
    """
    heading_text = CharBlock(classname='title', required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5')
    ], required=True)

    class Meta:
        icon = 'title'
        template = 'kdl_wagtail_core/blocks/heading_block.html'


class ImageBlock(BaseCaptionAttributionBlock):
    """
    `StructBlock` for using images with associated caption and attribution.
    """
    image = ImageChooserBlock(required=True)

    class Meta:
        icon = 'image'
        template = 'kdl_wagtail_core/blocks/image_block.html'


class GalleryBlock(StructBlock):
    images_block = ListBlock(ImageBlock())

    class Meta:
        icon = 'image'
        template = 'kdl_wagtail_core/blocks/gallery_block.html'


class LinkBlock(StructBlock):
    """
    `StructBlock` for using links to external URLs or internal pages.
    """
    url = URLBlock(required=False)
    page = PageChooserBlock(required=False)
    label = CharBlock()

    class Meta:
        help_text = """
        Use either URL or page, if both are filled in URL takes precedence.
        """
        icon = 'link'
        template = 'kdl_wagtail_core/blocks/link_block.html'


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    richtext_block = RichTextBlock(
        icon='pilcrow',
        template='kdl_wagtail_core/blocks/richtext_block.html'
    )
    document_block = DocumentBlock()
    gallery_block = GalleryBlock()
    image_block = ImageBlock()
    link_block = LinkBlock()
    embed_block = EmbedBlock()
    table_block = TableBlock()
