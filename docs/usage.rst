=====
Usage
=====

To use Django KDL Wagtail in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail.contrib.settings',
        ...
        'kdl_wagtail.core.apps.KdlWagtailCoreConfig',
        'kdl_wagtail.people.apps.KdlWagtailContribPeopleConfig',
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