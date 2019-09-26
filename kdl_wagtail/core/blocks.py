from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.core.blocks import (
    BooleanBlock, CharBlock, ChoiceBlock, ListBlock, PageChooserBlock
)
from wagtail.core.blocks import RichTextBlock as WagtailRichTextBlock
from wagtail.core.blocks import StreamBlock, StructBlock, StructValue, URLBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock as WagtailEmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class BaseStructBlock(StructBlock):
    show_in_menus = BooleanBlock(default=True, required=False)

    def get_form_context(self, value, prefix='', errors=None):
        context = super().get_form_context(value, prefix=prefix, errors=errors)
        fields = context['children'].copy()

        for field in reversed(context['children']):
            fields.move_to_end(field)

        context['children'] = fields

        return context


class AlignmentChoiceBlock(ChoiceBlock):
    choices = [
        ('', 'Select block alignment'),
        ('float-left', 'Left'),
        ('float-right', 'Right'),
        ('float-center', 'Centre'),
        ('full-width', 'Full width')
    ]


class RichTextBlock(WagtailRichTextBlock):
    class Meta:
        icon = 'pilcrow'
        template = 'kdl_wagtail_core/blocks/richtext_block.html'


class BaseCaptionAttributionBlock(BaseStructBlock):
    """
    Base `StructBlock` to create blocks that use captions and attribution
    fields.
    """
    transcription = RichTextBlock(required=False)
    description = RichTextBlock(required=False)

    attribution = CharBlock(required=False)
    caption = CharBlock(required=False)


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
    display = ChoiceBlock(choices=[
        ('', 'Select a display ratio'),
        ('widescreen', '16:9'),
        ('fourbythree', '4:3'),
        ('audio', 'Audio'),
        ('panorama', 'Panorama'),
        ('square', 'Square'),
        ('vertical', 'Vertical')
    ], required=False)
    embed_block = WagtailEmbedBlock(
        help_text='Insert an embed URL', icon='media')

    class Meta:
        icon = 'media'
        template = 'kdl_wagtail_core/blocks/embed_block.html'


class HeadingBlock(BaseStructBlock):
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


class LinkBlockStructValue(StructValue):
    def link(self):
        url = self.get('url')
        page = self.get('page')

        if url:
            return url
        elif page:
            return page.url


class ImageBlock(BaseCaptionAttributionBlock):
    """
    `StructBlock` for using images with associated caption and attribution.
    """
    page = PageChooserBlock(help_text='Link to a page', required=False)
    url = URLBlock(help_text='External link', required=False)
    alignment = AlignmentChoiceBlock(required=True)
    image = ImageChooserBlock(required=True)

    class Meta:
        help_text = """
        Use either URL or page links, if both are filled in the URL
        takes precedence.
        """
        icon = 'image'
        template = 'kdl_wagtail_core/blocks/image_block.html'
        value_class = LinkBlockStructValue


class GalleryBlock(BaseStructBlock):
    images_block = ListBlock(ImageBlock())

    class Meta:
        icon = 'image'
        template = 'kdl_wagtail_core/blocks/gallery_block.html'


class LinkBlock(BaseStructBlock):
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
        value_class = LinkBlockStructValue


class PullQuoteBlock(BaseStructBlock):
    quote = RichTextBlock()
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'openquote'
        template = 'kdl_wagtail_core/blocks/pullquote_block.html'


class TableBlock(BaseCaptionAttributionBlock):
    """
    `StructBlock` for using tables with associated caption and attribution.
    """
    table = WagtailTableBlock(required=True)

    class Meta:
        icon = 'table'
        template = 'kdl_wagtail_core/blocks/table_block.html'


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    richtext_block = RichTextBlock()
    document_block = DocumentBlock()
    gallery_block = GalleryBlock()
    image_block = ImageBlock()
    link_block = LinkBlock()
    pullquote_block = PullQuoteBlock()
    embed_block = EmbedBlock()
    table_block = TableBlock()
