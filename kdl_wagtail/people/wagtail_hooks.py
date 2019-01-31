from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Person


class PersonModelAdmin(ModelAdmin):
    model = Person
    list_display = ['name', 'title', 'thumbnail']
    menu_icon = 'group'


modeladmin_register(PersonModelAdmin)
