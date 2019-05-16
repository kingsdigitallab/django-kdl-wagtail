from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import get_bibliography_model


class BibliographyModelAdmin(ModelAdmin):
    model = get_bibliography_model()
    list_display = ['key', 'order', 'entry', 'note', 'shortnote']
    list_filter = ['author']
    menu_icon = 'form'
    search_fields = ['key', 'author', 'bib']


modeladmin_register(BibliographyModelAdmin)
