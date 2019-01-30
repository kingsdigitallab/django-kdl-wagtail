from django import template

from kdl_wagtail.core.models import FooterText

register = template.Library()


@register.inclusion_tag('kdl_wagtail/tags/footer_text.html',
                        takes_context=True)
def get_footer_text(context):
    footer_text = ''
    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().body

    return {'footer_text': footer_text}


@register.simple_tag()
def get_page_label(page):
    if not page:
        return

    return page.specific.content_type.model
