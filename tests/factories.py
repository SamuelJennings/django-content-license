"""factory_boy factories for the licensing models.

Tests build licences through these rather than calling ``objects.create()``
directly, so field defaults live in one place and uniqueness is handled for
them. ``License.name`` and ``License.canonical_url`` are both unique app-wide
and ``slug`` is derived from the name on save, so the factory drives all three
from a single sequence and repeated calls never collide.
"""

import factory

from licensing.models import License


class LicenseFactory(factory.django.DjangoModelFactory):
    """Build a saved :class:`License` with unique name, URL and derived slug."""

    class Meta:
        model = License

    name = factory.Sequence(lambda n: f"Test License {n}")
    canonical_url = factory.Sequence(lambda n: f"https://example.com/test-license-{n}")
    description = "A license for testing purposes"
    text = "This is the full text of the test license."
