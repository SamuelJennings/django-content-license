=====
Usage
=====

To use Django Content License in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'licensing.apps.LaboratoryConfig',
        ...
    )

Add Django Content License's URL patterns:

.. code-block:: python

    from licensing import urls as laboratory_urls


    urlpatterns = [
        ...
        url(r'^', include(laboratory_urls)),
        ...
    ]
