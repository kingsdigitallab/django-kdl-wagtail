=====
Usage
=====

To use Django KDL Wagtail in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail.contrib.settings',
        ...
        'kdl_wagtail.core',
        'kdl_wagtail.people',
        'kdl_wagtail.zotero',
        ...
    )

To use the Wagtail API, add Django KDL Wagtail's `api_router` to `urls.py`:

.. code-block:: python

    from kdl_wagtail.core.api import api_router
    urlpatterns = [
        ...
        path('api/v2/', api_router.urls),
        ...
        path('', include('wagtail.core.urls'))
    ]

Available settings:

.. code-block:: python

    # the number of items per page used by the pagination functions
    KDL_WAGTAIL_ITEMS_PER_PAGE = 10

    # the person model to be used by the kdl_wagtail.people app
    KDL_WAGTAIL_PERSON_MODEL = 'kdl_wagtail_people.Person'

    # Zotero bibliography settings
    # Zotero collection to import
    KDL_WAGTAIL_ZOTERO_COLLECTION = ''
    # ID of the Zotero library
    KDL_WAGTAIL_ZOTERO_LIBRARY_ID = ''
    # The type of library, either `group` or `user`
    KDL_WAGTAIL_ZOTERO_LIBRARY_TYPE = ''
    # Note citation style, for available styles see https://www.zotero.org/styles/
    KDL_WAGTAIL_ZOTERO_STYLE = 'chicago-note-bibliography'
    # Zotero API token
    KDL_WAGTAIL_ZOTERO_TOKEN = ''

Available commands:

To import bibliography entries from Zotero run the management command `zotero_import`.
Please note that this command does not deal with entries that have been deleted on the
Zotero side; it might be worth deleting all the Bibliography objects from the database
before running an import.
