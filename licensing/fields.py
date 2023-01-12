"""This module contains fields that you can use in your projects to link 
database items to a license contained in the `license.License` model. They don't
do anything special but are slightly more verbose when reading through
a Django model specification.

    from django.db import models
    from licensing.fields import LicenseFK, LicenseM2M

    class Dataset(models.Model):

        name = models.CharField()
        description = models.TextField()
        license = License()

"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class License(models.ForeignKey):
    """A foreign key field to the `license.License` model"""

    def __init__(self, *args, **kwargs):
        kwargs["to"] = "licensing.License"
        kwargs["verbose_name"] = _("license")
        super().__init__(*args, **kwargs)


class LicenseM2M(models.ManyToManyField):
    """A many-to-many field to the `license.License` model"""

    def __init__(self, *args, **kwargs):
        kwargs["to"] = "licensing.License"
        kwargs["verbose_name"] = _("licenses")
        super().__init__(*args, **kwargs)
