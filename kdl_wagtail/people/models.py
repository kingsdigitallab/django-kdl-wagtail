from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from kdl_wagtail.core.models import BaseIndexPage, BasePage
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel)
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class BasePerson(index.Indexed, ClusterableModel):
    """
    An abstract Django model for Person objects. It is meant to be used as a
    snippet to make the Person objects reusable and reduce duplication of code.
    Use the `@register_snippet` decorator to allow it to be accessible via the
    Snippets UI (e.g. /admin/snippets/kdl_wagtail_people/person/).
    `BasePerson` uses the `ClusterableModel`, which allows the relationship
    with another model to be stored locally to the 'parent' model
    (e.g. a PageModel) until the parent is explicitly saved. This allows the
    editor to use the 'Preview' button, to preview the content, without saving
    the relationships to the database.
    https://github.com/wagtail/django-modelcluster
    """
    _title = models.CharField('Title', max_length=254, blank=True, null=True)
    name = models.CharField('Name', max_length=254)

    introduction = models.TextField(
        blank=True, help_text='Short summary about the person')
    image = models.ForeignKey('wagtailimages.Image', null=True,
                              blank=True, on_delete=models.SET_NULL,
                              related_name='+')

    description = RichTextField(blank=True, help_text='Person bio/description')

    api_fields = [
        APIField('_title'),
        APIField('name'),
        APIField('introduction'),
        APIField('image'),
        APIField('description')
    ]

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('_title', classname='col6'),
                FieldPanel('name', classname='col6'),
            ])
        ], 'Name'),
        FieldPanel('introduction', 'full'),
        ImageChooserPanel('image'),
        FieldPanel('description', 'full')
    ]

    search_fields = [
        index.SearchField('name'),
        index.SearchField('introduction'),
        index.SearchField('description')
    ]

    class Meta:
        abstract = True
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return self.title

    @property
    def thumbnail(self):
        if self.image:
            return self.image.get_rendition('fill-50x50').img_tag()

        return None

    @property
    def title(self):
        return '{} {}'.format(
            self._title if self._title else '', self.name).strip()


@register_snippet
class Person(BasePerson):
    pass


def get_person_model():
    """
    Return the person model that is active in this project. Defaults to
    `kdl_wagtail_people.Person`.
    """
    try:
        return apps.get_model(
            settings.KDL_WAGTAIL_PERSON_MODEL, require_ready=False)
    except AttributeError:
        return Person
    except ValueError:
        raise ImproperlyConfigured(
            ('KDL_WAGTAIL_PERSON_MODEL must be of the form '
                '"app_label.model_name"')
        )
    except LookupError:
        raise ImproperlyConfigured(
            ('KDL_WAGTAIL_PERSON_MODEL refers to model "{}" '
                'that has not been installed'.format(
                    settings.KDL_WAGTAIL_PERSON_MODEL))
        )

    return Person


PersonModel = get_person_model()


class PeopleIndexPersonRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `Person` snippet and the
    `PeopleIndexPage` below. This allows Persons to be added to a
    PeopleIndexPage.
    """
    page = ParentalKey(
        'PeopleIndexPage', related_name='peopleindex_person_relationship',
        on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        PersonModel, related_name='person_peopleindex_relationship',
        on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('person')
    ]


class PeopleIndexPage(BaseIndexPage):
    api_fields = BaseIndexPage.api_fields + [
        APIField('peopleindex_person_relationship')
    ]

    content_panels = BaseIndexPage.content_panels + [
        InlinePanel('peopleindex_person_relationship',
                    label='People', panels=None, min_num=1)
    ]

    search_fields = BaseIndexPage.search_fields + [
        index.RelatedFields('peopleindex_person_relationship', [
            index.SearchField('person')
        ])
    ]

    def people(self):
        return self.peopleindex_person_relationship.all().select_related(
            'person')

    def get_context(self, request):
        context = super().get_context(request)
        context['people'] = self.people()

        return context


class PersonPage(BasePage):
    person = models.ForeignKey(
        PersonModel, related_name='pages', on_delete=models.PROTECT)

    api_fields = BasePage.api_fields + [
        APIField('person')
    ]

    content_panels = BasePage.content_panels + [
        SnippetChooserPanel('person')
    ]

    search_fields = BasePage.search_fields + [
        index.RelatedFields('person', Person.search_fields)
    ]
