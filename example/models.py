"""A model that carries a license."""

from django.db import models
from django.urls import reverse

from licensing.fields import LicenseField


class TestModel(models.Model):
    """A piece of content published under a license."""

    content_license = LicenseField()

    def get_absolute_url(self):
        """Return the detail page URL."""
        return reverse("example_detail", kwargs={"pk": self.pk})
