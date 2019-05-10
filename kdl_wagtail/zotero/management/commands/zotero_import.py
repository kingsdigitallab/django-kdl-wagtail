from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from kdl_wagtail.zotero.models import Bibliography
from pyzotero import zotero


class Command(BaseCommand):
    help = 'Imports bibliography records from Zotero'

    def handle(self, *args, **options):
        try:
            zot = zotero.Zotero(settings.KDL_WAGTAIL_ZOTERO_LIBRARY_ID,
                                settings.KDL_WAGTAIL_ZOTERO_LIBRARY_TYPE,
                                settings.KDL_WAGTAIL_ZOTERO_TOKEN,
                                preserve_json_order=True)
            collection_id = settings.KDL_WAGTAIL_ZOTERO_COLLECTION
            citation_style = settings.KDL_WAGTAIL_ZOTERO_STYLE

            self.import_bibliography(zot, collection_id, citation_style)
        except AttributeError as e:
            raise CommandError(e)

    def import_bibliography(self, zot, collection_id, citation_style):
        number_of_items = zot.count_items()

        self.stdout.write(
            '{} items in the zotero collection'.format(number_of_items))

        for idx, item in self.items_enumerator(
                zot, collection_id, citation_style):
            b, _ = Bibliography.objects.get_or_create(key=item['key'])
            b.order = idx
            b.citation = item['citation']
            b.url = item['links']['alternate']['href']
            b.bib = item['bib']
            b.save()

        self.stdout.write(
            self.style.SUCCESS('{} items imported/updated'.format(idx)))

    def items_enumerator(self, zot, collection_id, citation_style):
        return enumerate(
            zot.everything(
                zot.collection_items(
                    collection_id, include='bib,citation',
                    itemType='-attachment', order='creator',
                    style=citation_style)))
