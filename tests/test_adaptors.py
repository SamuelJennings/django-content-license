from django.test import TestCase
from licensing.adaptors import BibtexAdaptor, Crossref, Datacite, RISAdaptor
from licensing.adaptors.bibtex import parse
from licensing.exceptions import RemoteAdaptorError


class TestBibtex(TestCase):
    def setUp(self):

        with open("tests/data/publication.bib", "r") as f:
            self.file = f.read()

        entry = parse(self.file)
        self.entry = entry[0]

    def test_bibtex_parse(self):
        entry = parse(self.file)
        self.assertIsInstance(entry, list)

    # def test_bibtex_adaptor(self):
    # pprint(self.entry)
    # adaptor = BibtexAdaptor(self.entry)
    # adaptor.is_valid()
    # pprint(adaptor.cleaned_data)


class TestCrossref(TestCase):
    def setUp(self):
        self.adaptor = Crossref

    def test_valid_crossref_doi(self):
        doi = "10.1093/gji/ggz376"
        data, errors = self.adaptor(doi=doi).get_data()
        self.assertFalse(errors)

    def test_invalid_crossref_doi_raises(self):
        # this is a datacite DOI
        doi = "10.1594/pangaea.807217"
        self.assertRaises(RemoteAdaptorError, self.adaptor, doi=doi)


class TestDatacite(TestCase):
    def setUp(self):
        self.adaptor = Datacite

    # def test_valid_doi(self):
    #     doi = "10.1594/pangaea.807217"
    #     data, errors = self.adaptor(doi=doi).get_data()
    #     self.assertFalse(errors)

    def test_invalid_crossref_doi_raises(self):
        # this is a Crossref DOI
        doi = "10.1093/gji/ggz376"
        self.assertRaises(RemoteAdaptorError, self.adaptor, doi=doi)
