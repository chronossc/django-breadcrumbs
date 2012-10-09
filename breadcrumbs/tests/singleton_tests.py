# coding: utf-8

from django.test import TestCase

from breadcrumbs.breadcrumbs import Singleton


class Foo(Singleton):
    """
    Class used in singleton tests
    """
    pass


class SingletonTest(TestCase):

    def test_singleton(self):
        """
        Test singleton implementation with values
        """
        a = Foo()
        a.attr_1 = 1

        b = Foo()

        self.assertEqual(b.attr_1, 1)
        self.assertTrue(a is b, "'a' isn't 'b', Singleton not works")

    def test_singleton_destruction(self):
        """
        Test singleton imsinplementation with values and than destroy it
        """
        a = Foo()
        id_a = id(a)
        a.attr_1 = 1

        b = Foo()
        id_b = id(b)

        self.assertEqual(id_a, id_b)
        self.assertEqual(b.attr_1, 1)
        self.assertTrue(a is b, "'a' isn't 'b', Singleton not works")

        a._drop_it()

        c = Foo()
        id_c = id(c)
        self.assertNotEqual(id_a, id_c)
        self.assertNotEqual(getattr(c,'attr_1',None), 1)

