# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*-o!o*s(#p_^t1!&7n=e*++b$l#4-^(0#jtqpyn-032==)n9j)'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',

    'kdl_wagtail.core.apps.KdlWagtailCoreConfig',
    'kdl_wagtail.people.apps.KdlWagtailPeopleConfig',
]

SITE_ID = 1

MIDDLEWARE = ()
