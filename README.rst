=============================
Django KDL Wagtail
=============================

.. image:: https://badge.fury.io/py/django-kdl-wagtail.svg
    :target: https://badge.fury.io/py/django-kdl-wagtail

.. image:: https://travis-ci.org/kingsdigitallab/django-kdl-wagtail.svg?branch=master
    :target: https://travis-ci.org/kingsdigitallab/django-kdl-wagtail

.. image:: https://codecov.io/gh/kingsdigitallab/django-kdl-wagtail/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kingsdigitallab/django-kdl-wagtail

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
        'wagtail.contrib.settings',
        ...
        'kdl_wagtail.core',
        'kdl_wagtail.people',
        ...
    )

Features
--------

* A Core Wagtail application, `kdl_wagtail.core` with:
    * An abstract BasePage that contains and introduction and image fields, which all the other class in this package extend
    * A RichTextPage with just a RichTextField (WYSIWYG)
    * A StreamPage with a StreamField body
    * An abstract BaseIndexPage, with functions to return the page's live children, context, and a function to paginate the children
    * An IndexPage
    * A set of reusable StreamField blocks
    * Simple default templates for the pages and blocks defined in the module
* A public API based on Wagtail's API https://docs.wagtail.io/en/latest/advanced_topics/api/v2/configuration.html
* People application, `kdl_wagtail_people` with:
    * A Person snippet, this is accessible from the Wagtail menu bar
    * A PersonPage
    * A PeopleIndexPage
* Custom settings
    * Footer customisation
    * Analytics integration

TODO
----

* generic front end search page (with filters for tags, page types, ...)
* generic/abstract wagtail form page
    * contact us page (could possibly inherit from wagtail form page)
* FAQ page

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
