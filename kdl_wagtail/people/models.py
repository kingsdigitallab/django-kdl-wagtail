from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         MultiFieldPanel)
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class Person(index.Indexed, ClusterableModel):
    """
    A Django model to store Person objects.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/kdl_wagtail/person/)
    `Person` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """
    title = models.CharField('Title', max_length=254, blank=True, null=True)
    name = models.CharField('Name', max_length=254)

    image = models.ForeignKey('wagtailimages.Image', null=True,
                              blank=True, on_delete=models.SET_NULL,
                              related_name='+')

    summary = models.TextField(
        blank=True, help_text='Short summary about the person')
    description = RichTextField(blank=True, help_text='Person bio/description')

    api_fields = [
        APIField('title'),
        APIField('name'),
        APIField('image'),
        APIField('summary'),
        APIField('description')
    ]

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('title', classname='col6'),
                FieldPanel('name', classname='col6'),
            ])
        ], 'Name'),
        ImageChooserPanel('image'),
        FieldPanel('summary', 'full'),
        FieldPanel('description', 'full')
    ]

    search_fields = [
        index.SearchField('name'),
        index.SearchField('summary'),
        index.SearchField('description')
    ]

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return '{} {}'.format(self.title, self.name)

    @property
    def thumbnail(self):
        if self.image:
            return self.image.get_rendition('fill-50x50').img_tag()

        return None
