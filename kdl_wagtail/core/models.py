from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index

from .blocks import BaseStreamBlock
from .utils import paginate


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

        children = self._paginate(request)
        context['children'] = children

        return context

    def _paginate(self, request):
        return paginate(self.children(), request.GET.get('page'))


class IndexPage(BaseIndexPage):
    """
    A direct implementation of `BaseIndexPage`.
    """
    pass


class BaseRichTextPage(BasePage):
    """
    A base rich text page with a rich text field (WYSIWYG) body.
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

    class Meta:
        abstract = True


class RichTextPage(BaseRichTextPage):
    pass


class BaseStreamPage(BasePage):
    """
    A base rich text page with a stream field body with blocks defined in
    `blocks.BaseStreamBlock`.
    """
    body = StreamField(BaseStreamBlock(), verbose_name='Page body', blank=True)

    api_fields = BasePage.api_fields + [
        APIField('body')
    ]

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body')
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField('body')
    ]

    class Meta:
        abstract = True


class StreamPage(BaseStreamPage):
    pass


@register_setting
class AnalyticsSettings(BaseSetting):
    analytics_id = models.CharField(max_length=255)


@register_setting
class FooterSettings(BaseSetting):
    body = RichTextField()
