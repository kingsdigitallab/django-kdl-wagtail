=====
Usage
=====

To use Django KDL Wagtail in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'kdl_wagtail.apps.KdlWagtailConfig',
        ...
    )

Add Django KDL Wagtail's URL patterns:

.. code-block:: python

    from kdl_wagtail import urls as kdl_wagtail_urls


    urlpatterns = [
        ...
        url(r'^', include(kdl_wagtail_urls)),
        ...
    ]
