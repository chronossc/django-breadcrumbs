from setuptools import setup, find_packages
setup(
    name="django-breadcrumbs",
    version="1.1.2",
    packages=find_packages(exclude=('breadcrumbs_sample*', 'sample_d14*')),
    license='LICENSE',
    description="Easy to use generic breadcrumbs system for Django framework.",
    author="Felipe 'chronos' Prenholato",
    author_email="philipe.rp@gmail.com",
    url="http://github.com/chronossc/django-breadcrumbs",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=["Django>=1.2.7"],
)
