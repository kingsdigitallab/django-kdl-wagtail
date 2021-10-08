from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
    PageChooserPanel,
)
from wagtail.api import APIField
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
    FORM_FIELD_CHOICES,
    AbstractEmailForm,
    AbstractFormField,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Site
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


class BaseSearchPage(BasePage):
    '''
    A basic front-end search page for CMS content.
    It searches for live Wagtail pages matching a query passed in the query
    string. Results are paginated.

    TODO:
    add a facet for page types;
    templating mechanism for each result type;
    narrow down searchable page types with settings variable;
    include other wagtail content like images or documents?
        (might need to switch to Haystack for that)
    let user specify the order (relevance, date);
    '''
    class Meta:
        abstract = True

    def get_context(self, request, *args, **kwargs):
        ret = super(BaseSearchPage, self).get_context(request, *args, **kwargs)

        hits = self.get_search_hits(request)

        ret['hits'] = paginate(hits, request.GET.get('page', 1))
        ret['search_phrase'] = self.get_search_phrase(request)

        return ret

    def get_search_hits(self, request):
        query_set = self._get_querryset(request)
        ret = self._search_queryset(request, query_set)
        return ret

    def get_search_phrase(self, request):
        return request.GET.get('q', '').strip()

    def _get_querryset(self, request):
        ret = Page.objects.exclude(depth=1).live().specific()
        return ret

    def _search_queryset(self, request, queryset):
        from wagtail.search.query import MATCH_ALL
        phrase = self.get_search_phrase(request)
        if not phrase:
            phrase = MATCH_ALL
        ret = queryset.search(phrase)
        return ret


class SearchPage(BaseSearchPage):
    pass


class SitemapPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super(SitemapPage, self).get_context(
            request, *args, **kwargs)

        site = Site.find_for_request(request)
        if not site:
            return context

        context['children'] = site.root_page.get_children(
        ).live().order_by('title')

        return context


# --------------------------------------------------------------------------
#                   Form Builder & derived pages
# --------------------------------------------------------------------------


NEW_FIELD_CHOICES = []

''' This is ALWAYS available even if captcha app is not installed.
That's because django migrations take all choice options into consideration.
So we can't add option dynamically based on presence of captcha app.
'''
NEW_FIELD_CHOICES.append(('captcha', 'Captcha'))


class KDLFormBuilder(FormBuilder):
    '''
    Form builder with new field types:
    * captcha
    '''

    def create_captcha_field(self, field, options):
        '''
        This will raise an exception if captcha app isn't fully set up.
        Make sure you have installed dango-simple-captcha package,
        added 'captcha' to your INSTALLED_APPS
        anded a re_path(r'^captcha/', include('captcha.urls')) to urls.py.
        '''
        from captcha.fields import CaptchaField
        return CaptchaField(**options)


class KDLAbstractFormField(AbstractFormField):
    CHOICES = list(FORM_FIELD_CHOICES) + NEW_FIELD_CHOICES

    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        # use the choices tuple defined above
        choices=CHOICES
    )

    class Meta:
        abstract = True


class BaseFormBuilderPage(BasePage, AbstractEmailForm):
    '''
    An abstract Wagtail Form Builder.
    '''
    class Meta:
        abstract = True

    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('introduction', classname='full'),
        ImageChooserPanel('image')
    ] + [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    form_builder = KDLFormBuilder


class BaseContactUsPage(BaseFormBuilderPage):
    '''
    An abstract contact us page, inherit from generic form builder page.
    Nothing special here for the moment.
    '''
    class Meta:
        abstract = True


class ContactUsField(KDLAbstractFormField):
    '''
    Unfortunately we can't define this parental key against an abstract page
    '''
    page = ParentalKey('ContactUsPage', on_delete=models.CASCADE,
                       related_name='form_fields')


class ContactUsPage(BaseContactUsPage):
    pass


class ProxyPageAbstract(BasePage):
    '''
    Proxy to another page to help create external links and shortcuts in menus.
    Either on this site (Wagtail Page) or hosted on an external URL.
    When rendered this page will redirect to the target URL.
    '''
    target_page = models.ForeignKey(
        'wagtailcore.Page', null=True, blank=True,
        related_name='proxy_page', on_delete=models.SET_NULL
    )
    target_url = models.URLField('External URL', null=True, blank=True)

    class Meta:
        # description = 'A proxy to another page to make menu shortcuts.'
        abstract = True

    def clean(self):
        if not(bool(self.target_page) ^ bool(self.target_url)):
            raise ValidationError(
                'Please specify either a target page or URL.'
            )

    def get_url_parts(self, *args, **kwargs):
        '''Override this so this page work like an alias, faking its target.'''
        # Note: this function can't return external URLs
        ret = super(ProxyPageAbstract, self).get_url_parts(*args, **kwargs)
        if self.target_page:
            ret = self.target_page.get_url_parts(*args, **kwargs)
        return ret

    def get_absolute_target_url(self, request=None):
        '''Returns the URL of the target. None if not defined.'''
        ret = None
        if self.target_page:
            ret = self.target_page.get_full_url(request)
        if self.target_url:
            ret = self.target_url
        return ret

    def serve(self, request, *args, **kwargs):
        url = self.get_absolute_target_url(request)
        if url:
            ret = redirect(url, permanent=False)
        else:
            ret = super(ProxyPageAbstract, self).serve(
                request, *args, **kwargs
            )

        return ret

    content_panels = [
        FieldPanel('title', classname="full title"),
        PageChooserPanel('target_page'),
        FieldPanel('target_url'),
    ]


class ProxyPage(ProxyPageAbstract):
    # This should be in the base class but it won't work there.
    template = 'kdl_wagtail_core/base_page.html'

