#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-licensing
------------

Tests for `django-licensing` models module.
"""

from django.test import TestCase
from model_bakery import baker


class TestAuthor(TestCase):
    def setUp(self):
        self.author = baker.make(
            "licensing.Author",
            given="Sam",
            family="Jennings",
        )

    def test_str(self):
        self.assertEqual(f"{self.author}", self.author.given_family())

    def test_given_family(self):
        self.assertEqual(self.author.given_family(), "Sam Jennings")

    def test_family_given(self):
        self.assertEqual(self.author.family_given(), "Jennings, Sam")

    def test_g_family(self):
        self.assertEqual(self.author.g_family(), "S. Jennings")

    def test_family_g(self):
        self.assertEqual(self.author.family_g(), "Jennings, S.")

    def test_autocomplete_search_fields(self):
        autocomplete = self.author.autocomplete_search_fields()
        self.assertIn("family__icontains", autocomplete)
        self.assertIn("given__icontains", autocomplete)
        self.assertNotIn("test", autocomplete)


class TestLicensing(TestCase):
    def setUp(self):
        authors = baker.prepare("licensing.Author", family="Jennings", _quantity=1)
        self.pub = baker.make(
            "licensing.Licensing",
            title="This should be a really long title so we can test whether the uploaded pdf name is shortened properly using the simple_file_renamer",
            authors=authors,
            year=2022,
        )

    def test_str(self):
        self.assertEqual(str(self.pub), str(self.pub.label))

    def test_autocomplete_search_fields(self):
        autocomplete = self.pub.autocomplete_search_fields()
        self.assertIn("title__icontains", autocomplete)
        self.assertIn("authors__family__icontains", autocomplete)
        self.assertIn("label__icontains", autocomplete)
        self.assertNotIn("test", autocomplete)


class TestCollection(TestCase):
    def setUp(self):
        self.obj = baker.make(
            "licensing.Collection",
        )

    def test_str(self):
        self.assertEqual(str(self.obj), str(self.obj.name))


class TestLicensingAuthor(TestCase):
    def setUp(self):
        lit = baker.make("licensing.Licensing", year=2019)
        self.obj = baker.make("licensing.LicensingAuthor", licensing=lit)

    def test_str(self):
        self.assertEqual(str(self.obj), str(self.obj.position))
