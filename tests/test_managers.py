from pprint import pprint

from django.test import TestCase
from licensing.models import Author, Licensing


class TestLicensingManager(TestCase):
    def setUp(self):
        self.doi = "10.1093/gji/ggz376"
        self.manager = Licensing.objects

    def test_resolve_for_crossref_doi(self):
        doi = "10.1093/gji/ggz376"
        data, errors = Licensing.objects.resolve_doi(doi)

        # pprint(data)
        self.assertTrue("doi" in data.keys())
        self.assertFalse(errors)
        # self.assert
        # self.assertTrue("doi" in data.keys())
