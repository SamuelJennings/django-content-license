"""Convenience mixins for adding a license to your Django model."""

from .fields import License, LicenseM2M
from django.db import models


class LicensedModelMixin:
    """A mixin that adds a single license to each entry in your model. Adding a license is not required by default and `on_delete` is set to models.SET_NULL`.

    Example:

        class DatasetModel(LicensedModelMixin, models.Model):
            pass

    """

    license = License(on_delete=models.SET_NULL, null=True, blank=True)


class LicensedModel(LicensedModelMixin, models.Model):
    """The same as `LicensedModelMixin` but pre-mixes `django.db.models.Model`

    Example:

        class DatasetModel(LicensedModel):
            pass

    """

    pass


class MultiLicensedModelMixin:
    """A mixin that adds multiple licenses to each entry in your model. Adding
    a license is not required by default.

    Example:

        class DatasetModel(MultiLicensedModelMixin, models.Model):
            pass

    """

    license = LicenseM2M(blank=True)


class MultiLicensedModel(MultiLicensedModelMixin, models.Model):
    """The same as `MultiLicensedModelMixin` but pre-mixes `django.db.models.Model`

    Example:

        class DatasetModel(MultiLicensedModel):
            pass

    """

    pass
