=============================
Django KDL Wagtail
=============================

.. image:: https://badge.fury.io/py/django-kdl-wagtail.svg
    :target: https://badge.fury.io/py/django-kdl-wagtail

.. image:: https://travis-ci.org/jmiguelv/django-kdl-wagtail.svg?branch=master
    :target: https://travis-ci.org/jmiguelv/django-kdl-wagtail

.. image:: https://codecov.io/gh/jmiguelv/django-kdl-wagtail/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jmiguelv/django-kdl-wagtail

KDL Wagtail Base Models

Documentation
-------------

The full documentation is at https://django-kdl-wagtail.readthedocs.io.

Quickstart
----------

Install Django KDL Wagtail::

    pip install django-kdl-wagtail

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
