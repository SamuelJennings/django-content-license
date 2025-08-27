"""
Shared pytest fixtures for django-content-license tests.
"""
import pytest
from django.conf import settings

# pytest_plugins = ['django_pytest_plugin']


@pytest.fixture(scope='session')
def django_db_setup():
    """Set up test database."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }


@pytest.fixture
def license_data():
    """Standard license data for testing."""
    return {
        'name': 'Test License',
        'canonical_url': 'https://example.com/test-license',
        'description': 'A license for testing purposes',
        'text': 'This is the full text of the test license.',
    }


@pytest.fixture
def mit_license_data():
    """MIT license data for testing."""
    return {
        'name': 'MIT License',
        'canonical_url': 'https://opensource.org/licenses/MIT',
        'description': 'A permissive license that allows commercial use',
        'text': 'Permission is hereby granted, free of charge, to any person obtaining a copy...',
    }


@pytest.fixture
def gpl_license_data():
    """GPL license data for testing."""
    return {
        'name': 'GNU General Public License v3.0',
        'canonical_url': 'https://www.gnu.org/licenses/gpl-3.0.html',
        'description': 'A copyleft license that requires source code disclosure',
        'text': 'This program is free software: you can redistribute it and/or modify...',
    }


@pytest.fixture
def multiple_license_data(license_data, mit_license_data, gpl_license_data):
    """Multiple license data sets for testing."""
    return [license_data, mit_license_data, gpl_license_data]


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Automatically enable database access for all tests."""
    pass
