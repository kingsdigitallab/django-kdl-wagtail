from django import template

from kdl_wagtail.core.models import FooterSettings

register = template.Library()


@register.inclusion_tag(
    'kdl_wagtail/tags/footer_text.html', takes_context=True)
def get_footer_text(context):
    footer_text = ''

    request = context['request']
    if request:
        fs = FooterSettings.for_site(request.site)
        if fs:
            footer_text = fs.body

    return {'footer_text': footer_text}


@register.simple_tag()
def get_page_label(page):
    if not page:
        return

    return page.specific.content_type.model
