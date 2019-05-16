from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.safestring import mark_safe
from kdl_wagtail.core.models import BaseIndexPage
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class BaseBibliography(index.Indexed, ClusterableModel):
    key = models.CharField(max_length=32, unique=True)
    author = models.CharField(max_length=256, null=True)
    order = models.PositiveSmallIntegerField(null=True)
    citation = RichTextField(verbose_name='note')
    citation_short = RichTextField(null=True, verbose_name='shortnote')
    url = models.URLField()
    bib = RichTextField(verbose_name='bibliography entry')

    api_fields = [
        APIField('key'),
        APIField('author'),
        APIField('citation'),
        APIField('citation_short'),
        APIField('url'),
        APIField('bib')
    ]

    panels = [
        FieldPanel('key'),
        FieldPanel('url'),
        FieldPanel('author'),
        FieldPanel('bib'),
        FieldPanel('citation'),
        FieldPanel('citation_short')
    ]

    search_fields = [
        index.SearchField('author'),
        index.SearchField('citation'),
        index.SearchField('citation_short'),
        index.SearchField('bib')
    ]

    class Meta:
        abstract = True
        ordering = ['order']
        verbose_name = 'Biblography'
        verbose_name_plural = 'Bibliography'

    def __str__(self):
        return mark_safe(self.entry)

    @property
    def entry(self):
        return mark_safe(self.bib)

    @property
    def note(self):
        return mark_safe(self.citation)

    @property
    def shortnote(self):
        return mark_safe(self.citation_short)


@register_snippet
class Bibliography(BaseBibliography):
    pass


def get_bibliography_model():
    """
    Return the bibliography model that is active in this project. Defaults to
    `kdl_wagtail_zotero.Bibliography`.
    """
    try:
        return apps.get_model(
            settings.KDL_WAGTAIL_BIBLIOGRAPHY_MODEL, require_ready=False)
    except AttributeError:
        return Bibliography
    except ValueError:
        raise ImproperlyConfigured(
            ('KDL_WAGTAIL_BIBLIOGRAPHY_MODEL must be of the form '
                '"app_label.model_name"')
        )
    except LookupError:
        raise ImproperlyConfigured(
            ('KDL_WAGTAIL_BIBLIOGRAPHY_MODEL refers to model "{}" '
                'that has not been installed'.format(
                    settings.KDL_WAGTAIL_BIBLIOGRAPHY_MODEL))
        )

    return Bibliography


BibliographyModel = get_bibliography_model()


class BibliographyIndexPage(BaseIndexPage):
    def entries(self):
        return BibliographyModel.objects.all()

    def get_context(self, request):
        context = super().get_context(request)
        context['entries'] = self.entries()

        return context
