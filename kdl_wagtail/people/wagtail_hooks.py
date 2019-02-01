from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import get_person_model


class PersonModelAdmin(ModelAdmin):
    model = get_person_model()
    list_display = ['name', 'title', 'thumbnail']
    menu_icon = 'group'


modeladmin_register(PersonModelAdmin)
