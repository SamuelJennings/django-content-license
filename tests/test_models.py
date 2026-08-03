"""Tests for the License model in django-content-license."""

import datetime
import time

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from licensing.models import License
from tests.factories import LicenseFactory

# The deprecation rules only care whether a date is set, never which one. A fixed
# date keeps the parametrize arguments (evaluated at collection) and the assertions
# (evaluated later) from straddling a midnight boundary in a long CI run.
DEPRECATION_DATE = datetime.date(2026, 1, 1)


class TestLicense:
    """Field values, uniqueness constraints, and computed properties."""

    def test_license_creation_with_all_fields(self):
        license_obj = LicenseFactory(
            name="MIT License",
            canonical_url="https://opensource.org/licenses/MIT",
            description="A permissive license that allows for commercial use.",
            text="Permission is hereby granted, free of charge...",
        )

        assert license_obj.name == "MIT License"
        assert license_obj.canonical_url == "https://opensource.org/licenses/MIT"
        assert license_obj.description == "A permissive license that allows for commercial use."
        assert license_obj.text == "Permission is hereby granted, free of charge..."
        assert license_obj.is_active is True  # Default value
        assert license_obj.deprecated_date is None  # Default value
        assert license_obj.created_at is not None
        assert license_obj.updated_at is not None
        assert license_obj.slug == "mit-license"  # Auto-generated

    def test_license_creation_minimal_fields(self):
        license_obj = LicenseFactory(
            name="Test License",
            canonical_url="https://example.com/test-license",
            text="This is the license text.",
            description=None,
        )

        assert license_obj.name == "Test License"
        assert license_obj.canonical_url == "https://example.com/test-license"
        assert license_obj.description is None  # Null field
        assert license_obj.text == "This is the license text."
        assert license_obj.is_active is True

    @pytest.mark.parametrize(
        "field, value",
        [
            ("name", "Duplicate Name License"),
            ("canonical_url", "https://example.com/duplicate"),
        ],
    )
    def test_uniqueness_constraint(self, field, value):
        LicenseFactory(**{field: value})

        with pytest.raises(Exception):  # IntegrityError or ValidationError
            LicenseFactory(**{field: value})

    def test_str_method(self, mit_license):
        assert str(mit_license) == "MIT License"

    def test_repr_method(self, mit_license):
        assert repr(mit_license) == "<License: MIT License>"

    def test_full_name_property(self, mit_license):
        assert mit_license.full_name == "MIT License"

    @pytest.mark.parametrize(
        "description, expected",
        [
            (
                "A permissive license that allows for commercial use.",
                "A permissive license that allows for commercial use.",
            ),
            ("A" * 150, "A" * 100 + "..."),
            ("", "No description"),
        ],
    )
    def test_short_description_property(self, description, expected):
        license_obj = LicenseFactory(description=description)
        assert license_obj.short_description == expected

    @pytest.mark.parametrize(
        "is_active, expected",
        [
            (True, "Active"),
            (False, "Deprecated"),
        ],
    )
    def test_status_display_property(self, is_active, expected):
        license_obj = LicenseFactory(is_active=is_active)
        assert license_obj.status_display == expected

    def test_deprecated_date_field(self):
        deprecated_date = datetime.date(2023, 1, 1)
        license_obj = LicenseFactory(deprecated_date=deprecated_date, is_active=False)
        assert license_obj.deprecated_date == deprecated_date


class TestLicenseSlug:
    """Slug auto-generation, uniqueness, and preservation on save."""

    def test_slug_auto_generation(self):
        license_obj = LicenseFactory(
            name="Creative Commons BY 4.0",
            canonical_url="https://creativecommons.org/licenses/by/4.0/",
        )
        assert license_obj.slug == "creative-commons-by-40"

    def test_slug_unique_constraint_with_counter(self):
        LicenseFactory(name="Test License")

        # Same slug-generating name, different special characters.
        license2 = LicenseFactory(name="Test License!!!")

        assert license2.slug == "test-license-1"

    def test_manual_slug_is_preserved(self):
        license_obj = LicenseFactory(name="MIT License", slug="custom-mit-slug")
        assert license_obj.slug == "custom-mit-slug"

    def test_slug_with_special_characters(self):
        license_obj = LicenseFactory(name="GPL-3.0+")
        assert license_obj.slug == "gpl-30"

    def test_slug_update_on_save(self):
        license_obj = LicenseFactory(name="BSD License", slug="original-slug")

        # Clear the slug and save.
        license_obj.slug = ""
        license_obj.save()

        # Slug should be regenerated.
        assert license_obj.slug == "bsd-license"

    def test_slug_generation_with_empty_name_fallback(self):
        license_obj = LicenseFactory(name="!!!")  # Doesn't generate a valid slug
        assert license_obj.slug == "license"

    def test_slug_generation_preserves_existing_on_update(self):
        license_obj = LicenseFactory(name="Original Name")
        original_slug = license_obj.slug

        license_obj.text = "Updated text"
        license_obj.save()

        assert license_obj.slug == original_slug

    def test_slug_generation_with_multiple_conflicts(self):
        license1 = LicenseFactory(name="Conflict Test 1")
        license2 = LicenseFactory(name="Conflict Test 2")
        license3 = LicenseFactory(name="Conflict Test 3")

        slugs = [license1.slug, license2.slug, license3.slug]

        assert len(slugs) == len(set(slugs))

    def test_slug_update_avoids_self_conflict(self):
        license_obj = LicenseFactory(name="Self Conflict Test")
        original_slug = license_obj.slug

        # Update the license (which triggers save and slug generation).
        license_obj.text = "Updated text"
        license_obj.save()

        # Should keep the same slug, not add a counter.
        assert license_obj.slug == original_slug


@pytest.fixture
def three_licenses():
    """Three saved licences spanning active, deprecated, and CC states."""
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


class TestLicenseQuerySet:
    """Querysets and class methods over multiple licenses."""

    def test_get_recommended_licenses(self, three_licenses):
        active, deprecated, cc = three_licenses
        recommended = License.get_recommended_licenses()

        # Should only include active licenses.
        assert active in recommended
        assert cc in recommended
        assert deprecated not in recommended

        # Should be ordered by name.
        license_names = [license.name for license in recommended]
        assert license_names == sorted(license_names)

    def test_ordering_by_name(self, three_licenses):
        licenses = License.objects.all()
        license_names = [license.name for license in licenses]
        assert license_names == sorted(license_names)

    def test_filtering_by_is_active(self, three_licenses):
        active_licenses = License.objects.filter(is_active=True)
        assert active_licenses.count() == 2

        deprecated_licenses = License.objects.filter(is_active=False)
        assert deprecated_licenses.count() == 1

    def test_declared_indexes(self):
        """The fields the lookup paths rely on are actually indexed.

        The previous version of this test built two querysets and asserted
        nothing. Querysets are lazy, so it never reached the database and could
        only have failed if a field name disappeared. The index declaration on
        Meta is the thing worth guarding, so assert against that directly.
        """
        indexed = {tuple(index.fields) for index in License._meta.indexes}

        assert ("is_active",) in indexed
        assert ("slug",) in indexed


class TestLicenseValidation:
    """full_clean() and clean() validation behaviour."""

    @pytest.mark.parametrize(
        "overrides",
        [
            {"name": ""},
            {"canonical_url": ""},
            {"text": ""},
            {"canonical_url": "not-a-valid-url"},
            {"name": "A" * 256},  # Exceeds max_length=255
            {"canonical_url": "https://example.com/" + "a" * 500},  # Exceeds max_length=500
        ],
    )
    def test_full_clean_validation_errors(self, overrides):
        fields = {
            "name": "Test License",
            "canonical_url": "https://example.com/test",
            "text": "License text",
        }
        fields.update(overrides)
        license_obj = LicenseFactory.build(**fields)

        with pytest.raises(ValidationError):
            license_obj.full_clean()

    def test_deprecated_license_without_date_validation(self):
        license_obj = LicenseFactory.build(
            name="Deprecated License",
            canonical_url="https://example.com/deprecated",
            text="Deprecated license text",
            is_active=False,  # Deprecated but no deprecated_date
        )

        with pytest.raises(ValidationError) as excinfo:
            license_obj.clean()

        assert "deprecated_date" in excinfo.value.error_dict
        assert "Deprecated licenses must have a deprecated date" in str(excinfo.value.error_dict["deprecated_date"][0])

    def test_active_license_with_deprecated_date_validation(self):
        license_obj = LicenseFactory.build(
            name="Active License",
            canonical_url="https://example.com/active",
            text="Active license text",
            is_active=True,
            deprecated_date=DEPRECATION_DATE,  # Active but has deprecated_date
        )

        with pytest.raises(ValidationError) as excinfo:
            license_obj.clean()

        assert "deprecated_date" in excinfo.value.error_dict
        assert "Active licenses should not have a deprecated date" in str(
            excinfo.value.error_dict["deprecated_date"][0]
        )

    @pytest.mark.parametrize(
        "overrides",
        [
            {"is_active": False, "deprecated_date": DEPRECATION_DATE},
            {"is_active": True},
        ],
    )
    def test_clean_passes_for_consistent_state(self, overrides):
        fields = {
            "name": "Consistent License",
            "canonical_url": "https://example.com/consistent",
            "text": "Consistent license text",
        }
        fields.update(overrides)
        license_obj = LicenseFactory.build(**fields)

        license_obj.clean()  # Should not raise


class TestLicenseTimestamps:
    """created_at / updated_at auto-population."""

    def test_created_at_auto_now_add(self):
        before_creation = timezone.now()
        license_obj = LicenseFactory()
        after_creation = timezone.now()

        assert license_obj.created_at is not None
        assert license_obj.created_at >= before_creation
        assert license_obj.created_at <= after_creation

    def test_updated_at_auto_now(self):
        license_obj = LicenseFactory()
        original_updated_at = license_obj.updated_at

        # Small delay to ensure timestamp difference.
        time.sleep(0.01)

        license_obj.description = "Updated description"
        license_obj.save()

        assert license_obj.updated_at > original_updated_at

    def test_created_at_unchanged_on_update(self):
        license_obj = LicenseFactory()
        original_created_at = license_obj.created_at

        license_obj.description = "Updated description"
        license_obj.save()

        assert license_obj.created_at == original_created_at
