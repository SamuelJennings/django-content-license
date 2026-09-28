"""The LicenseField model field."""

from functools import partialmethod

from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import html_snippet


class LicenseField(models.ForeignKey):
    """A foreign key to `License` that adds an attribution method to its model.

    Declaring `license = LicenseField()` on a model adds `get_license_display()`, which
    renders the attribution snippet for the instance. Keyword arguments are passed to
    `ForeignKey`; `to` is always `licensing.License`, and `on_delete` defaults to `PROTECT`.
    """

    def __init__(self, *args, **kwargs):
        kwargs["to"] = "licensing.License"
        kwargs.setdefault("on_delete", models.PROTECT)
        kwargs.setdefault("verbose_name", _("license"))
        kwargs.setdefault(
            "help_text", _("The license under which this content is published")
        )
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        """Add `get_<name>_display()` to the model unless it defines its own."""
        super().contribute_to_class(cls, name, **kwargs)
        method_name = f"get_{self.name}_display"
        if method_name not in cls.__dict__:
            setattr(
                cls,
                method_name,
                partialmethod(html_snippet, field_name=self.name),
            )
