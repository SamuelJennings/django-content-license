from django.db import models
from django.urls import reverse

from licensing.fields import License


class TestModel(models.Model):
    license = License()

    def get_absolute_url(self):
        return reverse("example_detail", kwargs={"pk": self.pk})
