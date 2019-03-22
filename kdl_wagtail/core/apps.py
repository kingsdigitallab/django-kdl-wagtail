from django.apps import AppConfig, apps


class KdlWagtailCoreConfig(AppConfig):
    name = 'kdl_wagtail.core'
    label = 'kdl_wagtail_core'

    def ready(self):
        self.hide_page_types()

    def hide_page_types(self):
        '''Hide some Wagtail Pages types from the create new child page screen.

        The page types to hide are specified in your settings.py as a list of
        django content types <app_label>.<model_name>.

        KDL_WAGTAIL_HIDDEN_PAGE_TYPES = [
            'kdl_wagtail_core.streampage',
        ]

        # select * from django_content_type;
        '''

        from django.conf import settings

        @classmethod
        def clean_parent_page_models(cls):
            return []

        page_types = getattr(settings, 'KDL_WAGTAIL_HIDDEN_PAGE_TYPES', [])

        for page_type in page_types:
            PageClass = apps.get_model(page_type)
            PageClass.clean_parent_page_models = clean_parent_page_models
