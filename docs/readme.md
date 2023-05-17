# Django Licensing 

[![Github Build](https://github.com/SSJenny90/django-licensing/actions/workflows/build.yml/badge.svg)](https://github.com/SSJenny90/django-licensing/actions/workflows/build.yml)
[![Github Docs](https://github.com/SSJenny90/django-licensing/actions/workflows/docs.yml/badge.svg)](https://github.com/SSJenny90/django-licensing/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/SSJenny90/django-licensing/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/SSJenny90/django-licensing)
![GitHub](https://img.shields.io/github/license/SSJenny90/django-licensing)
![GitHub last commit](https://img.shields.io/github/last-commit/SSJenny90/django-licensing)
![PyPI](https://img.shields.io/pypi/v/django-licensing)
<!-- [![RTD](https://readthedocs.org/projects/django-licensing/badge/?version=latest)](https://django-licensing.readthedocs.io/en/latest/readme.html) -->
<!-- [![Documentation](https://github.com/SSJenny90/django-licensing/actions/workflows/build-docs.yml/badge.svg)](https://github.com/SSJenny90/django-licensing/actions/workflows/build-docs.yml) -->
<!-- [![PR](https://img.shields.io/github/issues-pr/SSJenny90/django-licensing)](https://github.com/SSJenny90/django-licensing/pulls)
[![Issues](https://img.shields.io/github/issues-raw/SSJenny90/django-licensing)](https://github.com/SSJenny90/django-licensing/pulls) -->
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/django-licensing) -->
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/django-licensing) -->

A scientific licensing management app for Django

Documentation
-------------

The full documentation is at https://ssjenny90.github.io/django-licensing/

Quickstart
----------

Install Django Licensing::

    pip install django-licensing

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'licensing',
        ...
    )

Add Django Licensing's URL patterns:

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

