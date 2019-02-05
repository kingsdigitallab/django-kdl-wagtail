#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-kdl-wagtail
------------

Tests for `django-kdl-wagtail` core module.
"""

from django.test import TestCase
from kdl_wagtail.core.utils import paginate


class TestKdl_wagtail_core(TestCase):

    def setUp(self):
        pass

    def test_paginate(self):
        items = list(range(20))
        pages = paginate(items)

        self.assertEquals(2, pages.paginator.num_pages)
        self.assertEquals(20, pages.paginator.count)

    def test_paginate_no_items(self):
        self.assertIsNone(paginate(None))

    def test_paginate_invalid_parameters(self):
        items = list(range(20))
        pages = paginate(items, page='a')

        self.assertIsNotNone(pages)
        self.assertEquals(2, pages.paginator.num_pages)
        self.assertEquals(20, pages.paginator.count)

        with self.assertRaises(ValueError):
            paginate(items, page_size='a')

    def tearDown(self):
        pass
