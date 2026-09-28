"""Django app configuration for the example project."""

from django.apps import AppConfig


class ExampleConfig(AppConfig):
    """Register the example app."""

    name = "example"
    default_auto_field = "django.db.models.BigAutoField"
