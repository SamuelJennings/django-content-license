from functools import partialmethod

from django.test import TestCase
from example.models import TestModel  # replace with your actual model name

from licensing.fields import License
from licensing.models import License as LicenseModel


class LicenseFieldTest(TestCase):
    def setUp(self):
        self.license = LicenseModel.objects.create(
            name="Test License",
            URL="http://example.com/license",
            description="This is a test license",
            text="This is a test license",
        )
        self.model_instance = TestModel.objects.create(license=self.license)

    def test_license_field_creation(self):
        self.assertEqual(self.model_instance.license, self.license)  # replace with an actual License instance

    # def test_get_license_display_method(self):
    #     self.assertTrue(hasattr(self.model_instance, "get_license_display"))
    #     self.assertIsInstance(self.model_instance.get_license_display, partialmethod)
