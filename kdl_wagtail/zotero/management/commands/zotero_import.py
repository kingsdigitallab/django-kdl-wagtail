from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from kdl_wagtail.zotero.models import Bibliography
from pyzotero import zotero


class Command(BaseCommand):
    help = 'Imports bibliography records from Zotero'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete existing bibliography entries before doing an import'
        )

    def handle(self, *args, **options):
        try:
            zot = zotero.Zotero(settings.KDL_WAGTAIL_ZOTERO_LIBRARY_ID,
                                settings.KDL_WAGTAIL_ZOTERO_LIBRARY_TYPE,
                                settings.KDL_WAGTAIL_ZOTERO_TOKEN,
                                preserve_json_order=True)
            collection_id = settings.KDL_WAGTAIL_ZOTERO_COLLECTION
            citation_styles = {
                'note': settings.KDL_WAGTAIL_ZOTERO_NOTE_STYLE,
                'shortnote': settings.KDL_WAGTAIL_ZOTERO_SHORTNOTE_STYLE
            }

            if options['delete']:
                self.delete_bibliography()
                self.stdout.write('')

            self.import_bibliography(zot, collection_id, citation_styles)
        except AttributeError as e:
            raise CommandError(e)

    def delete_bibliography(self):
        number_of_entries = Bibliography.objects.count()
        if number_of_entries == 0:
            self.stdout.write(
                self.style.NOTICE('No bibliography entries to delete'))
            return

        self.stdout.write(
            self.style.WARNING(
                'Deleting bibliography entries that are not being used'))

        for b in Bibliography.objects.all():
            if not b.get_usage():
                b.delete()

    def import_bibliography(self, zot, collection_id, citation_styles):
        self.stdout.write('Importing bibliography entries from Zotero')

        for key in citation_styles.keys():
            citation_style = citation_styles[key]

            for idx, item in self.items_enumerator(
                    zot, collection_id, citation_style):
                b, _ = Bibliography.objects.get_or_create(key=item['key'])

                if 'creatorSummary' in item['meta']:
                    b.author = item['meta']['creatorSummary']

                b.order = idx

                if key == 'shortnote':
                    b.citation_short = item['citation']
                else:
                    b.citation = item['citation']

                b.url = item['links']['alternate']['href']
                b.bib = item['bib']
                b.save()

        self.stdout.write(
            self.style.SUCCESS('{} bibliography entries imported'.format(idx)))

    def items_enumerator(self, zot, collection_id, citation_style):
        return enumerate(
            zot.everything(
                zot.collection_items(
                    collection_id, include='bib,citation,data',
                    itemType='-attachment', order='creator',
                    style=citation_style)))
