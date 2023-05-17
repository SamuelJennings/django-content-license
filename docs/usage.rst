=====
Usage
=====

To use Django Licensing in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'licensing.apps.LaboratoryConfig',
        ...
    )

Add Django Licensing's URL patterns:

.. code-block:: python

    from licensing import urls as laboratory_urls


    urlpatterns = [
        ...
        url(r'^', include(laboratory_urls)),
        ...
    ]
