from django import template
from django.conf import settings
from django.template.defaultfilters import striptags, truncatechars
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from kdl_wagtail.core.models import AnalyticsSettings, FooterSettings
from kdl_wagtail.core.utils import paginate

register = template.Library()


@register.simple_tag(takes_context=True)
def get_analytics_id(context):
    analytics_id = ''

    request = context['request']
    if request:
        s = AnalyticsSettings.for_site(request.site)
        if s:
            analytics_id = s.analytics_id

    return {'analytics_id': analytics_id}


@register.simple_tag()
def get_block_title(block):
    if not block:
        return

    if block.block_type == 'document_block':
        if block.value.get('caption'):
            return block.value.get('caption')

        return block.value.get('document').title

    if block.block_type == 'embed_block':
        if block.value.get('caption'):
            return block.value.get('caption')

        return block.value.get('embed_block').url.split('/')[2]

    if block.block_type == 'heading_block':
        return block.value.get('heading_text')

    if block.block_type == 'image_block':
        if block.value.get('caption'):
            return block.value.get('caption')

        return block.value.get('image').title

    if block.block_type == 'gallery_block':
        return 'Image gallery'

    if block.block_type == 'link_block':
        return block.value.get('label')

    if block.block_type == 'pullquote_block':
        return striptags(
            truncatechars(block.value.get('quote').source.__str__(), 20))

    if block.block_type == 'richtext_block':
        return striptags(truncatechars(block.value.source.__str__(), 20))

    if block.block_type == 'table_block':
        if block.value.get('caption'):
            return block.value.get('caption')

        return 'Table'

    return block.block_type.replace('_', ' ')


@register.inclusion_tag(
    'kdl_wagtail_core/tags/footer_text.html', takes_context=True)
def get_footer_text(context):
    footer_text = ''

    request = context['request']
    if request:
        s = FooterSettings.for_site(request.site)
        if s:
            footer_text = s.body

    return {'footer_text': footer_text}


@register.simple_tag(takes_context=True)
def get_page_children(context, page):
    if not page:
        return None

    request = context['request']
    if not request:
        return None

    return paginate(
        page.get_children().specific.live(), request.GET.get('page'))


@register.simple_tag()
def get_page_label(page):
    if not page:
        return None

    return page.specific.content_type.model


@register.simple_tag()
def get_object_id(obj, prefix=None, suffix=None):
    """Return the 'identity' of an object. This is an integer which is
    guaranteed to be unique and constant for this object during its lifetime.
    Two objects with non-overlapping lifetimes may have the same id() value.
    See https://docs.python.org/3/library/functions.html#id
    """
    obj_id = getattr(obj, 'id', id(obj))

    if prefix:
        obj_id = '{}-{}'.format(prefix, obj_id)

    if suffix:
        obj_id = '{}-{}'.format(obj_id, suffix)

    return obj_id


@register.filter()
def krackdown(text):
    filters = getattr(settings, 'KDL_WAGTAIL_KRACKDOWN_FILTERS', [])

    if not isinstance(text, str):
        text = text.__html__()

    for function_name in filters:
        # not catching import errors to allow the propagation of the error
        f = import_string(function_name)
        text = f(text)

    return mark_safe(text)


@register.filter()
def order_by(value, arg):
    return value.order_by(arg)
