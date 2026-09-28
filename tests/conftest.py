"""Shared pytest fixtures for django-content-license tests."""

import datetime

import pytest

from tests.factories import LicenseFactory

# Never override `django_db_setup`: pytest-django's own fixture creates the schema.


@pytest.fixture
def license_obj():
    return LicenseFactory()


@pytest.fixture
def mit_license():
    return LicenseFactory(
        name="MIT License",
        canonical_url="https://opensource.org/licenses/MIT",
        description="A permissive license that allows commercial use",
        text="Permission is hereby granted, free of charge, to any person obtaining a copy...",
    )


@pytest.fixture
def gpl_license():
    return LicenseFactory(
        name="GNU General Public License v3.0",
        canonical_url="https://www.gnu.org/licenses/gpl-3.0.html",
        description="A copyleft license that requires source code disclosure",
        text="This program is free software: you can redistribute it and/or modify...",
    )


@pytest.fixture
def licenses(license_obj, mit_license, gpl_license):
    return [license_obj, mit_license, gpl_license]


@pytest.fixture
def cc_by_license():
    return LicenseFactory(
        name="Creative Commons BY 4.0",
        canonical_url="https://creativecommons.org/licenses/by/4.0/",
        text="CC BY license text",
        description="Allows others to distribute and build upon the material",
    )


@pytest.fixture
def apache_license():
    return LicenseFactory(
        name="Apache License 2.0",
        canonical_url="https://www.apache.org/licenses/LICENSE-2.0",
        text="Apache 2.0 license text",
        description="A permissive license with patent protection",
    )


@pytest.fixture
def three_licenses():
    active = LicenseFactory(
        name="MIT License",
        canonical_url="https://opensource.org/licenses/MIT",
        text="MIT license text",
        is_active=True,
    )
    deprecated = LicenseFactory(
        name="Old License",
        canonical_url="https://example.com/old",
        text="Old license text",
        is_active=False,
        deprecated_date=datetime.date(2020, 1, 1),
    )
    cc = LicenseFactory(
        name="Creative Commons BY 4.0",
        canonical_url="https://creativecommons.org/licenses/by/4.0/",
        text="CC BY license text",
        is_active=True,
    )
    return active, deprecated, cc


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
