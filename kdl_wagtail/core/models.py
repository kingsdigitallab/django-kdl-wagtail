from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .blocks import BaseStreamBlock


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. It is made accessible in
    the templates via the template tag `get_footer_text` defined in
    `kdl_wagtail/templatetags/kdl_wagtail_core_tags.py`.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/kdl_wagtail_core/footertext/)
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name_plural = 'Footer Text'

    def __str__(self):
        return 'Footer text'


class BasePage(Page):
    """
    A base page model, to be extended, it contains two default fields, an
    introduction text field and an image.
    """
    introduction = models.TextField(
        help_text='Text to describe the page', blank=True
    )
    image = models.ForeignKey(
        Image, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='+'
    )

    api_fields = [
        APIField('introduction'),
        APIField('image')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname='full'),
        ImageChooserPanel('image')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('introduction')
    ]

    class Meta:
        abstract = True


class BaseIndexPage(BasePage):
    """
    A base index page model.
    """
    class Meta:
        abstract = True

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super().get_context(request)

        children = self.paginate(request, self.children())

        context['children'] = children

        return context

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(
            self.children(), settings.KDL_WAGTAIL_ITEMS_PER_PAGE)

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        return pages


class RichTextPage(BasePage):
    """
    A rich text page with a rich text field (WYSIWYG) body.
    """
    body = RichTextField()

    api_fields = BasePage.api_fields + [
        APIField('body')
    ]

    content_panels = BasePage.content_panels + [
        FieldPanel('body', classname='full')
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField('body')
    ]


class StreamPage(BasePage):
    """
    A rich text page with a stream field body with blocks defined in
    `blocks.BaseStreamBlock`.
    """
    body = StreamField(BaseStreamBlock(), verbose_name='Page body', blank=True)

    api_fields = BasePage.api_fields + [
        APIField('body')
    ]

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body', classname='full')
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField('body')
    ]
