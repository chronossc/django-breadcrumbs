#!/usr/bin/env python

import os, sys

from django.conf import settings


if not settings.configured:
    settings_dict = dict(
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'django.contrib.flatpages',
            'breadcrumbs',
            ),
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3"
                }
            },
        )

    settings.configure(**settings_dict)


def runtests(*test_args):

    if not test_args:
        test_args = ['breadcrumbs']

    # try to set more used args to django test
    test_kwargs = {
        'verbosity': 1,
        'noinput': False,
        'failfast': False,
    }
    for i,arg in enumerate(sys.argv):
        if arg.startswith('-v'):
            _value = arg.replace('-v','')
            if len(_value):
                test_kwargs['verbosity'] = int(_value)
            else:
                test_kwargs['verbosity'] = int(sys.argv[i+1])
        if arg == '--noinput':
            test_kwargs['noinput'] = True
        if arg == '--failfast':
            test_kwargs['failfast'] =True

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(
        interactive=True, **test_kwargs).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
