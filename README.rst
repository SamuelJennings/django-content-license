=============================
Django Licensing
=============================

.. image:: https://badge.fury.io/py/django-licensing.svg
    :target: https://badge.fury.io/py/django-licensing

.. image:: https://travis-ci.org/SSJenny90/django-licensing.svg?branch=master
    :target: https://travis-ci.org/SSJenny90/django-licensing

.. image:: https://codecov.io/gh/SSJenny90/django-licensing/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/SSJenny90/django-licensing

A scientific licensing management app for Django

Documentation
-------------

The full documentation is at https://django-licensing.readthedocs.io.

Quickstart
----------

Install Django Licensing::

    pip install django-licensing

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'licensing.apps.LicensingConfig',
        ...
    )

Add Django Licensing's URL patterns:

.. code-block:: python

    from licensing import urls as licensing_urls


    urlpatterns = [
        ...
        url(r'^', include(licensing_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
