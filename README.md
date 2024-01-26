# Django Content License

[![Github Build](https://github.com/SSJenny90/django-content-license/actions/workflows/build.yml/badge.svg)](https://github.com/SSJenny90/django-content-license/actions/workflows/build.yml)
[![Github Tests](https://github.com/SSJenny90/django-content-license/actions/workflows/tests.yml/badge.svg)](https://github.com/SSJenny90/django-content-license/actions/workflows/tests.yml)
![GitHub](https://img.shields.io/github/license/SSJenny90/django-content-license)
![GitHub last commit](https://img.shields.io/github/last-commit/SSJenny90/django-content-license)
<!-- ![PyPI](https://img.shields.io/pypi/v/django-content-license) -->

Django Content License is a simple app that allows you to associate a content license with a model instance and display appropriate attribution in your HTML templates.

## What's included?

### License Model

A simple `License` model that can be associated with any other model in your project. The `License` model stores the following information:

* name: The name of the license (e.g. CC-BY-4.0, CC0 1.0, MIT, etc.)
* description: A description of the license
* text: The full text of the license
* URL: A Canonical URL for the license

### LicenseField

A `LicenseField` that subclasses `ForeignKey` and points towards the `licensing.License` model.

* Sets default translatable verbose_name and help_text for the field
* Sets default on_delete behavior of `models.PROTECT` to ensure that licenses cannot be deleted if they are associated with any database entries
* Adds a get_FOO_display method to the model that returns an HTML snippet containing attribution information for the associated database entry


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

add a `LicenseField` to any of your models:

    from django.db import models
    from licensing.models import LicenseField

    class MyModel(models.Model):
        ...
        license = LicenseField()
        ...

then, make sure to run `makemigrations` and `migrate` to apply the changes to your database.

That's it. Now you can access the license information for any instance of your model in your templates:

    {{ mymodel.get_license_display }}


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
