from django import template
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
    obj_id = id(obj)

    if prefix:
        obj_id = '{}-{}'.format(prefix, obj_id)

    if suffix:
        obj_id = '{}-{}'.format(obj_id, suffix)

    return obj_id
