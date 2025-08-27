from django.db import models
from django.urls import reverse

from licensing.fields import LicenseField


class TestModel(models.Model):
    license = LicenseField()

    def get_absolute_url(self):
        return reverse("example_detail", kwargs={"pk": self.pk})
