# Django Content License

[![Github Build](https://github.com/Geoluminate/django-content-license/actions/workflows/build.yml/badge.svg)](https://github.com/Geoluminate/django-content-license/actions/workflows/build.yml)
[![Github Tests](https://github.com/Geoluminate/django-content-license/actions/workflows/tests.yml/badge.svg)](https://github.com/Geoluminate/django-content-license/actions/workflows/tests.yml)
![GitHub](https://img.shields.io/github/license/Geoluminate/django-content-license)
![GitHub last commit](https://img.shields.io/github/last-commit/Geoluminate/django-content-license)
<!-- ![PyPI](https://img.shields.io/pypi/v/django-content-license) -->

Django Content License is a simple app that allows you to associate a content license with a model instance and display appropriate attribution in your HTML templates.

> [!NOTE]
> There is already a published package similar in purpose to this one: [django-licensing](https://pypi.org/project/django-licensing/). Please see the [quick comparison](#comparison-with-django-licensing) below for why I chose to create a new one.

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


## Quickstart

Install Django Content License:

    pip install django-content-license

Add it to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'licensing',
        ...
    )

add a `LicenseField` to any of your models:

    from django.db import models
    from licensing.field import LicenseField

    class MyModel(models.Model):
        ...
        license = LicenseField()
        ...

then, make sure to run `makemigrations` and `migrate` to apply the changes to your database.

That's it. Now you can access the license information for any instance of your model in your templates:

    {{ mymodel.get_license_display }}


## Comparison with `django-licensing`

`django-licensing` is a package that provides similar functionality to this package. It was created some 10 years ago, was last released in 2014 and last updated in 2020. Regardless, it probably gets the job done in most cases. However, there were some implementation details that I didn't site well with me and some more capabilities that I wanted to add.

### Things I didn't like

* It require you to subclass an abstract `Licensed` model in your own project.
* The `Licensed` model provides a FK to the `License` model which hardcodes the `on_delete` to `models.CASCADE`. This means that if your DB admin deletes a license (perhaps by mistake), they will also delete any database entries that are associated with that license. Yikes!
* `django-licensing` does not store the full license text. Having the full text allows us to provide the entire license with any content downloads.
* No descriptions of licenses provided.
* Included initial data are long outdated.

### What this package does instead

* Include licenses in your models via a custom Django field, rather than subclassing an abstract model.
* Provide sensible field defaults for `verbose_name`, `help_text`, and `on_delete` which can all be overridden if desired.
* `on_delete` defaults to `models.PROTECT` to ensure that licenses cannot be accidentally deleted if they are associated with existing database entries.
* Provide a default `get_FOO_display` method that returns an HTML snippet containing attribution information for the associated database entry.
* Store the full license text in the database.
* Provide helpful description of each license.
* Provides initial data that includes the latest Creative Commons licenses (v4.0).

## Contributing

Check out the the contributing guidelines in [CONTRIBUTING.md](CONTRIBUTING.md) for more details on how to contribute to this project.

## Credits

See [AUTHORS.md](AUTHORS.md) for a list of contributors to this project and appropriate credits.
