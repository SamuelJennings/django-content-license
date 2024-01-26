# Django Content License 

[![Github Build](https://github.com/SSJenny90/django-content-license/actions/workflows/build.yml/badge.svg)](https://github.com/SSJenny90/django-content-license/actions/workflows/build.yml)
[![Github Docs](https://github.com/SSJenny90/django-content-license/actions/workflows/docs.yml/badge.svg)](https://github.com/SSJenny90/django-content-license/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/SSJenny90/django-content-license/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/SSJenny90/django-content-license)
![GitHub](https://img.shields.io/github/license/SSJenny90/django-content-license)
![GitHub last commit](https://img.shields.io/github/last-commit/SSJenny90/django-content-license)
![PyPI](https://img.shields.io/pypi/v/django-content-license)
<!-- [![RTD](https://readthedocs.org/projects/django-content-license/badge/?version=latest)](https://django-content-license.readthedocs.io/en/latest/readme.html) -->
<!-- [![Documentation](https://github.com/SSJenny90/django-content-license/actions/workflows/build-docs.yml/badge.svg)](https://github.com/SSJenny90/django-content-license/actions/workflows/build-docs.yml) -->
<!-- [![PR](https://img.shields.io/github/issues-pr/SSJenny90/django-content-license)](https://github.com/SSJenny90/django-content-license/pulls)
[![Issues](https://img.shields.io/github/issues-raw/SSJenny90/django-content-license)](https://github.com/SSJenny90/django-content-license/pulls) -->
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/django-content-license) -->
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/django-content-license) -->

A scientific licensing management app for Django

Documentation
-------------

The full documentation is at https://ssjenny90.github.io/django-content-license/

Quickstart
----------

Install Django Content License::

    pip install django-content-license

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'licensing',
        ...
    )

Add Django Content License's URL patterns:

    urlpatterns = [
        ...
        path('', include("licensing.urls")),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

