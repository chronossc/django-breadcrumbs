# # coding: utf-8

# import os
# from django.conf import settings
# from django.test import TestCase

# from breadcrumbs.breadcrumbs import (Breadcrumb, Breadcrumbs,
#     BreadcrumbsInvalidFormat, BreadcrumbsNotSet)

# class BreadcrumbsTest(TestCase):

#     def setUp(self):
#         self.old_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
#         breadcrumbs_middleware_class = 'breadcrumbs.middleware.BreadcrumbsMiddleware'
#         if breadcrumbs_middleware_class not in settings.MIDDLEWARE_CLASSES:
#             settings.MIDDLEWARE_CLASSES += (breadcrumbs_middleware_class,)
#         self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
#         settings.TEMPLATE_DIRS = (
#             os.path.join(
#                 os.path.dirname(__file__),
#                 'templates'
#             ),
#         )
#         # self.old_LOGIN_URL = settings.LOGIN_URL
#         # settings.LOGIN_URL = '/accounts/login/'

#         # now we start singleton
#         self.breadcrumbs = Breadcrumbs()

#     def tearDown(self):
#         settings.MIDDLEWARE_CLASSES = self.old_MIDDLEWARE_CLASSES
#         settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS
#         # settings.LOGIN_URL = self.old_LOGIN_URL

#         # kill singleton
#         Breadcrumbs('a','/a')
#         Breadcrumbs('b','/b')
#         print Breadcrumbs()
#         self.breadcrumbs._drop_it()
#         del(self.breadcrumbs)
#         Breadcrumbs('c','/c')
#         print Breadcrumbs()

#     def test_breadcrumb_class(self):
#         b = Breadcrumb("Home", "/")
#         self.assertEqual(b.name, "Home")
#         self.assertEqual(b.url, "/")

#     def test_breadcrumbs_singleton(self):
#         brd = Breadcrumbs()
#         brd('a', '/a/')
#         brd('b', '/b/')


