=====
Usage
=====

To use Django KDL Wagtail in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'kdl_wagtail.core.apps.KdlWagtailCoreConfig',
        'kdl_wagtail.contrib.people.apps.KdlWagtailContribPeopleConfig',
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
