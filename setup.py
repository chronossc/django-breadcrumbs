from setuptools import setup, find_packages
setup(
    name="django-breadcrumbs",
    version="1.1.3",
    packages=find_packages(exclude=('breadcrumbs_sample*', 'sample_d14*')),
    author="Felipe 'chronos' Prenholato",
    author_email="philipe.rp@gmail.com",
    mainteiner="Felipe 'chronos' Prenholato",
    mainteiner_email="philipe.rp@gmail.com",
    url="http://github.com/chronossc/django-breadcrumbs",
    license='NEW BSD LICENSE: http://www.opensource.org/licenses/bsd-license.php',
    description="Easy to use generic breadcrumbs system for Django framework.",
    long_description="*django-breadcrumbs* is a breadcrumb system to Django "
        "framework that allow you to add custom breadcrumbs for simple views, "
        "generic views and support Django FlatPages app. It works as a "
        "pluggable middleware that add a breadcrumbs callable/iterable in your "
        "request object, allowing you to set  breadcrumbs (one or more) in "
        "each view accepting objects, lists or tuples added from "
        "request.breadcrumbs and is iterable, easy to use in templates "
        "providing a object with name and url attributes.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=["Django>=1.3.4"],
)
