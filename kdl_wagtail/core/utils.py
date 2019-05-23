import json
import re

from django.conf import settings
from django.contrib.contenttypes.management import create_contenttypes
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder


def paginate(items, page=1, page_size=10):
    if not items:
        return None

    if hasattr(settings, 'KDL_WAGTAIL_ITEMS_PER_PAGE'):
        page_size = settings.KDL_WAGTAIL_ITEMS_PER_PAGE

    paginator = Paginator(items, page_size)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return pages


def migrate_wagtail_page_type(apps, schema_editor, mapping):
    '''
    Fairly generic method to convert all instances of one direct subtype
    of wagtail page into another.

    Returns the number of converted pages.

    This is supposed to be called from a data migration operation function.

    https://docs.djangoproject.com/en/2.2/topics/migrations/#data-migrations

    Method:

    A record from the specific Page type table is copied into the new type
    table. But the parent record in wagtailcore_page is left intact
    (same id, title, slug, webpath) apart from its content_type.

    All fields with the same names are automatically copied. Other fields and
    custom transforms can be done in a custom copy function
    attached to the 'mapping' dictionary.

    An OPTIONAL 'select' entry in 'mapping' links to a function that can
    further filter the default django queryset of all pages to convert.

    IT IS RECOMMENDED TO BACK UP YOUR DATABASE BEFORE USING THIS FUNCTION.

    Example:

    def my_migration_operation(apps, schema_editor):

        def copy(page_from, page_to):
            page_to.field_a = page_from.field_b

        def select(qs):
            return qs.filter(title__icontains='banana')

        mapping = {
            'models': {
                'from': ('kdl_wagtail_page', 'RichPage'),
                'to': ('kdl_wagtail_core', 'RichTextPage'),
            },
            'copy': copy,
            'select': select,
        }

        convert_pages(apps, schema_editor, mapping)

    '''

    PageRevision = apps.get_model('wagtailcore', 'PageRevision')
    PageFrom = apps.get_model(*mapping['models']['from'])
    PageTo = apps.get_model(*mapping['models']['to'])

    # see ClusterableModel.to_json()
    def to_json(page):
        from wagtail.core.models import Page
        return json.dumps(Page.serializable_data(page), cls=DjangoJSONEncoder)

    pages_to = []

    pages_from = PageFrom.objects.all()
    select = mapping.get('select', None)
    if select:
        pages_from = select(pages_from)

    if pages_from.count() < 1:
        return pages_to

    copy = mapping.get('copy', None)

    # make sure all content_types are present in the DB
    # see https://stackoverflow.com/a/42791235/3748764
    from django.apps import apps as global_apps
    create_contenttypes(
        global_apps.get_app_config(mapping['models']['to'][0]),
        verbosity=0, interactive=False
    )

    # get the content type of PageTo
    ContentType = apps.get_model('contenttypes', 'ContentType')
    content_type_to = ContentType.objects.filter(
        app_label=mapping['models']['to'][0],
        model=mapping['models']['to'][1].lower()
    ).first()

    for page_from in pages_from:
        page_to = PageTo()

        # naive conversion: we copy all the fields which have a common name
        # this will at least copy all the fields from Page table
        # See wagtail.core.models.Page.copy()
        for field in page_to._meta.get_fields():
            # Ignore reverse relations
            if field.auto_created:
                continue

            # Ignore m2m relations - they will be copied as child objects
            # if modelcluster supports them at all (as it does for tags)
            if field.many_to_many:
                continue

            if hasattr(page_from, field.name):
                setattr(page_to, field.name, getattr(
                    page_from, field.name, None
                ))

        # particular cases
        page_to.id = page_from.id
        page_to.page_ptr_id = page_from.page_ptr_id
        page_to.content_type_id = content_type_to.pk

        # custom copy
        if copy:
            copy(page_from, page_to)

        pages_to.append(page_to)

        # now convert the latest revision (if any)
        page_rev = PageRevision.objects.filter(
            page_id=page_to.id
        ).order_by('-created_at', '-id').first()
        if page_rev:
            page_rev.content_json = to_json(page_to)
            page_rev.save()

    # Remove all the converted page
    # we use a raw statement instead of .delete() because we want to keep
    # the parent Page record.
    # TODO: for large number of ids, we might need to process this in chunk.
    # TODO: ANY in the the where clause may not work with other RDBMS than psql
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(
            'DELETE FROM {} WHERE page_ptr_id = ANY(%s)'.format(
                PageFrom._meta.db_table),
            [[p.page_ptr_id for p in pages_to]]
        )

    # now we can save the converted pages (without duplicate values)
    for page_to in pages_to:
        page_to.save()

    return len(pages_to)


def krackdown_anchor(html):
    return re.sub(
        r'\{#([^\}]+)\}', r'<a id="\1"></a>', html)


def krackdown_link(html):
    return re.sub(
        r'\[([^\[]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)


def krackdown_footnote(html):
    return re.sub(
        r'\[\^([^\]]+)\]',
        r'<sup id="fnref:\1"><a href="#fn:\1">\1</a></sup>', html)
