from functools import partialmethod

from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


def get_license_attribution(model_instance):
    attr = {
        "title": str(model_instance),
        "link": model_instance.get_absolute_url(),
        "creators": "Unknown",
        "creators_link": None,
    }

    return attr


def get_license_creator(model_instance):
    return model_instance.creator


def html_snippet(model_instance, field_name):
    license = getattr(model_instance, field_name)  # noqa: A001
    snippet = render_to_string("licensing/snippet.html", {"object": model_instance, "license": license})
    return mark_safe(snippet)  # noqa: S308


class LicenseField(models.ForeignKey):
    """A custom foreign key field pointing to the License model"""

    def __init__(self, *args, **kwargs):
        kwargs["to"] = "licensing.License"
        kwargs.setdefault("on_delete", models.PROTECT)
        kwargs.setdefault("verbose_name", _("license"))
        kwargs.setdefault("help_text", _("the license under which this content is published"))
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        method_name = f"get_{self.name}_display"
        if method_name not in cls.__dict__:
            setattr(
                cls,
                method_name,
                partialmethod(html_snippet, field_name=self.name),
            )
