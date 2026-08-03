"""Shared pytest fixtures for django-content-license tests.

Object construction goes through :mod:`tests.factories`; the fixtures here wrap
those factories so a test asks for what it needs rather than assembling it.
"""

import pytest

from tests.factories import LicenseFactory

# NOTE: do not override `django_db_setup` here. pytest-django's built-in fixture
# creates the test database AND runs migrations; overriding it to only swap the
# DATABASES dict (as a previous version did) leaves the schema uncreated and
# every DB test fails with "no such table". The DB is configured in
# tests/settings.py; let pytest-django own setup.


@pytest.fixture
def license_obj():
    """A saved :class:`~licensing.models.License` with default test values."""
    return LicenseFactory()


@pytest.fixture
def mit_license():
    """A saved licence carrying the MIT metadata used across the suite."""
    return LicenseFactory(
        name="MIT License",
        canonical_url="https://opensource.org/licenses/MIT",
        description="A permissive license that allows commercial use",
        text="Permission is hereby granted, free of charge, to any person obtaining a copy...",
    )


@pytest.fixture
def gpl_license():
    """A saved licence carrying the GPL metadata used across the suite."""
    return LicenseFactory(
        name="GNU General Public License v3.0",
        canonical_url="https://www.gnu.org/licenses/gpl-3.0.html",
        description="A copyleft license that requires source code disclosure",
        text="This program is free software: you can redistribute it and/or modify...",
    )


@pytest.fixture
def licenses(license_obj, mit_license, gpl_license):
    """Three saved licences, for tests that need more than one row."""
    return [license_obj, mit_license, gpl_license]


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Automatically enable database access for all tests."""
