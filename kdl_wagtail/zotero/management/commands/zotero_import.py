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
                                settings.KDL_WAGTAIL_ZOTERO_TOKEN)
            self.import_bibliography(zot)
        except AttributeError as e:
            raise CommandError(e)

    def import_bibliography(self, zot):
        number_of_items = zot.count_items()

        self.stdout.write('{} items to import/update'.format(number_of_items))

        for item in self.items_generator(zot):
            b, _ = Bibliography.objects.get_or_create(key=item['key'])
            b.citation = item['citation']
            b.url = item['links']['alternate']['href']
            b.bib = item['bib']
            b.save()

        self.stdout.write(self.style.SUCCESS(
            '{} items imported/updated'.format(number_of_items)))

    def items_generator(self, zot):
        for item in zot.everything(zot.items(include='bib,citation')):
            yield item
