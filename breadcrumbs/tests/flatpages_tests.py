# coding: utf-8
import os
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.test import TestCase
from django.utils.datastructures import SortedDict
from breadcrumbs.breadcrumbs import Breadcrumb, Breadcrumbs


class FlatpagesTest(TestCase):
    fixtures = ['sample_flatpages_for_breadcrumbs.json']

    def setUp(self):
        breadcrumbs_middleware_class = 'breadcrumbs.middleware.BreadcrumbsMiddleware'
        flatpages_middleware_class = 'breadcrumbs.middleware.FlatpageFallbackMiddleware'

        # remove breadcrumbs middlewares to assert that we set correct
        # order
        self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES = [mid for mid \
            in self.old_MIDDLEWARE_CLASSES if mid not in \
                (breadcrumbs_middleware_class, flatpages_middleware_class)]
        settings.MIDDLEWARE_CLASSES += [
            breadcrumbs_middleware_class,
            flatpages_middleware_class
        ]
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(
                os.path.dirname(__file__),
                'templates'
            ),
        )
        # now we start singleton. singleton are tested on singleton_tests.py
        self.breadcrumbs = Breadcrumbs()

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES

        # kill singleton
        self.breadcrumbs._drop_it()

    def test_flatpages_fixture_loaded(self):
        flat1 = FlatPage.objects.get(pk=1)
        self.assertEqual(flat1.title, u"Flat Page 1")
        self.assertEqual(flat1.content, u"This is flat 1")
        flat2 = FlatPage.objects.get(pk=2)
        self.assertEqual(flat2.title, u"Flat page 2")
        self.assertEqual(flat2.content, u"This is flat 2 under flat 1")

    def test_404_flatpage(self):
        response = self.client.get('/404_not_found/')
        self.assertEqual(response.status_code, 404)
        # self.assertContains(response, "<p>Isn't it flat!</p>")

    def test_fallback_flatpage(self):
        response = self.client.get('/flat01/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            '<ul id="breadcrumbs"><li><a href="/flat01/">Flat Page 1</a></li></ul>')

        response = self.client.get('/flat01/flat02/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
            '<ul id="breadcrumbs"><li><a href="/flat01/">Flat Page 1</a> &raquo; </li><li><a href="/flat01/flat02/">Flat page 2</a></li></ul>')
