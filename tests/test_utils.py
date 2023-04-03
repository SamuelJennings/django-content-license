from datetime import datetime

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from licensing import utils
from model_bakery import baker


class TestUtils(TestCase):
    def setUp(self):
        authors = baker.prepare("licensing.Author", family="Jennings", _quantity=1)
        self.pub = baker.make(
            "licensing.Licensing",
            title="This should be a really long title so we can test whether the uploaded pdf name is shortened properly using the simple_file_renamer",
            authors=authors,
            year=2022,
        )

    def test_datadict_resolves_mapping(self):
        """Test that DataDict items can be resolved by original key
        or new key provided my mappingkey kwarg"""
        data = utils.DataDict(
            {"x_original": 8, "y": {"z": 5}},
            keymap={
                "x": "x_original",
                "y": "y.z",
            },
        )
        self.assertEquals(data["x"], 8)
        self.assertEquals(data["x_original"], 8)

    def test_clean_doi(self):
        doi = "10.1093/gji/ggz376"
        clean = utils.clean_doi
        self.assertEqual(doi, clean(doi))
        self.assertEqual(doi, clean("doi.org/10.1093/gji/ggz376"))
        self.assertEqual(doi, clean("https://doi.org/10.1093/gji/ggz376"))
        self.assertEqual(doi, clean("http://doi.org/10.1093/gji/ggz376"))
        self.assertEqual(doi, clean("www.doi.org/10.1093/gji/ggz376"))

    def test_simple_autolabeler(self):
        label = utils.simple_autolabeler(self.pub)
        self.assertEquals(label, "Jennings2022")
        self.pub.label = label
        self.pub.save()
        new_pub = baker.make(
            "licensing.Licensing",
            label="test",
            authors=self.pub.authors.all(),
            year=2022,
        )
        label = utils.simple_autolabeler(new_pub)
        self.assertEquals(label, "Jennings2022b")

    def test_get_current_year(self):
        year = utils.get_current_year()
        self.assertEqual(datetime.now().year, year)

    def test_simple_file_renamer(self):
        new_name = utils.pdf_file_renamer(self.pub)
        self.assertEqual(new_name, "licensing/" + self.pub.title[:50].strip() + ".pdf")
        self.assertEqual(len(new_name), 64)
