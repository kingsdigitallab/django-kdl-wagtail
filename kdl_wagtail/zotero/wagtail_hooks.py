from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import get_bibliography_model


class BibliographyModelAdmin(ModelAdmin):
    model = get_bibliography_model()
    list_display = ['key', 'order', 'note', 'entry']
    menu_icon = 'form'


modeladmin_register(BibliographyModelAdmin)
