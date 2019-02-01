#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-kdl-wagtail
------------

Tests for `django-kdl-wagtail` people module.
"""

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from kdl_wagtail.people.models import Person, get_person_model


class TestKdl_wagtail_people(TestCase):

    def setUp(self):
        pass

    def test_get_person_model(self):
        self.assertEqual(get_person_model(), Person)

    @override_settings(
        KDL_WAGTAIL_PERSON_MODEL='kdl_wagtail_people.Person')
    def test_swappable_person_model(self):
        self.assertEqual(get_person_model(), Person)

    @override_settings(KDL_WAGTAIL_PERSON_MODEL='invalid_classpath')
    def test_swappable_person_model_invalid_setting(self):
        self.assertRaises(ImproperlyConfigured, get_person_model)

    @override_settings(KDL_WAGTAIL_PERSON_MODEL='nonexisting.Model')
    def test_swappable_person_model_nonexisting_model(self):
        self.assertRaises(ImproperlyConfigured, get_person_model)

    def tearDown(self):
        pass
