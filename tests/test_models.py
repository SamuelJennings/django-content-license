from django.test import TestCase

from licensing.models import License


class LicenseModelTest(TestCase):
    def setUp(self):
        self.license = License.objects.create(
            name="Test License",
            URL="http://example.com/license",
            description="This is a test license",
            text="This is a test license",
        )

    def test_license_creation(self):
        self.assertEqual(self.license.name, "Test License")
        self.assertEqual(self.license.URL, "http://example.com/license")
        self.assertEqual(self.license.description, "This is a test license")
        self.assertEqual(self.license.text, "This is a test license")
        self.assertEqual(self.license.slug, "test-license")

    def test_string_representation(self):
        self.assertEqual(str(self.license), self.license.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(License._meta.verbose_name_plural), "licenses")
