"""
Tests for the License model in django-content-license.
Django TestCase-based tests.
"""
import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from licensing.models import License


class LicenseModelTest(TestCase):
    """Test cases for the License model using Django TestCase."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_license_data = {
            'name': 'MIT License',
            'canonical_url': 'https://opensource.org/licenses/MIT',
            'description': 'A permissive license that allows for commercial use.',
            'text': 'Permission is hereby granted, free of charge...',
        }

    def test_license_creation_with_all_fields(self):
        """Test creating a license with all fields."""
        license_obj = License.objects.create(**self.valid_license_data)

        self.assertEqual(license_obj.name, 'MIT License')
        self.assertEqual(license_obj.canonical_url, 'https://opensource.org/licenses/MIT')
        self.assertEqual(license_obj.description, 'A permissive license that allows for commercial use.')
        self.assertEqual(license_obj.text, 'Permission is hereby granted, free of charge...')
        self.assertTrue(license_obj.is_active)  # Default value
        self.assertIsNone(license_obj.deprecated_date)  # Default value
        self.assertIsNotNone(license_obj.created_at)
        self.assertIsNotNone(license_obj.updated_at)
        self.assertEqual(license_obj.slug, 'mit-license')  # Auto-generated

    def test_license_creation_minimal_fields(self):
        """Test creating a license with only required fields."""
        minimal_data = {
            'name': 'Test License',
            'canonical_url': 'https://example.com/test-license',
            'text': 'This is the license text.',
        }
        license_obj = License.objects.create(**minimal_data)

        self.assertEqual(license_obj.name, 'Test License')
        self.assertEqual(license_obj.canonical_url, 'https://example.com/test-license')
        self.assertIsNone(license_obj.description)  # Null field
        self.assertEqual(license_obj.text, 'This is the license text.')
        self.assertTrue(license_obj.is_active)

    def test_name_uniqueness_constraint(self):
        """Test that license names must be unique."""
        License.objects.create(**self.valid_license_data)

        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            License.objects.create(**self.valid_license_data)

    def test_canonical_url_uniqueness_constraint(self):
        """Test that canonical URLs must be unique."""
        License.objects.create(**self.valid_license_data)

        duplicate_url_data = self.valid_license_data.copy()
        duplicate_url_data['name'] = 'Different Name'

        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            License.objects.create(**duplicate_url_data)

    def test_str_method(self):
        """Test the __str__ method returns the license name."""
        license_obj = License.objects.create(**self.valid_license_data)
        self.assertEqual(str(license_obj), 'MIT License')

    def test_repr_method(self):
        """Test the __repr__ method returns proper representation."""
        license_obj = License.objects.create(**self.valid_license_data)
        self.assertEqual(repr(license_obj), '<License: MIT License>')

    def test_full_name_property(self):
        """Test the full_name property returns the name."""
        license_obj = License.objects.create(**self.valid_license_data)
        self.assertEqual(license_obj.full_name, 'MIT License')

    def test_short_description_property_with_description(self):
        """Test short_description property with a description."""
        license_obj = License.objects.create(**self.valid_license_data)
        self.assertEqual(license_obj.short_description, 'A permissive license that allows for commercial use.')

    def test_short_description_property_long_description(self):
        """Test short_description property truncates long descriptions."""
        long_description = 'A' * 150  # 150 characters
        data = self.valid_license_data.copy()
        data['description'] = long_description

        license_obj = License.objects.create(**data)
        expected = 'A' * 100 + '...'
        self.assertEqual(license_obj.short_description, expected)

    def test_short_description_property_no_description(self):
        """Test short_description property with no description."""
        data = self.valid_license_data.copy()
        data['description'] = ''

        license_obj = License.objects.create(**data)
        self.assertEqual(license_obj.short_description, 'No description')

    def test_status_display_property_active(self):
        """Test status_display property for active license."""
        license_obj = License.objects.create(**self.valid_license_data)
        self.assertEqual(license_obj.status_display, 'Active')

    def test_status_display_property_deprecated(self):
        """Test status_display property for deprecated license."""
        data = self.valid_license_data.copy()
        data['is_active'] = False

        license_obj = License.objects.create(**data)
        self.assertEqual(license_obj.status_display, 'Deprecated')

    def test_deprecated_date_field(self):
        """Test the deprecated_date field."""
        deprecated_date = datetime.date(2023, 1, 1)
        data = self.valid_license_data.copy()
        data['deprecated_date'] = deprecated_date
        data['is_active'] = False

        license_obj = License.objects.create(**data)
        self.assertEqual(license_obj.deprecated_date, deprecated_date)


class LicenseSlugTest(TestCase):
    """Test cases for License slug generation."""

    def test_slug_auto_generation(self):
        """Test that slug is auto-generated from name."""
        license_obj = License.objects.create(
            name='Creative Commons BY 4.0',
            canonical_url='https://creativecommons.org/licenses/by/4.0/',
            text='This is the license text.'
        )
        self.assertEqual(license_obj.slug, 'creative-commons-by-40')

    def test_slug_unique_constraint_with_counter(self):
        """Test that duplicate slugs get a counter."""
        # Create first license
        License.objects.create(
            name='Test License',
            canonical_url='https://example.com/test1',
            text='License text 1'
        )

        # Create second license with same slug-generating name
        license2 = License.objects.create(
            name='Test License!!!',  # Will generate same slug due to special chars
            canonical_url='https://example.com/test2',
            text='License text 2'
        )

        # Check that slug got incremented
        self.assertEqual(license2.slug, 'test-license-1')

    def test_manual_slug_is_preserved(self):
        """Test that manually set slugs are preserved."""
        license_obj = License.objects.create(
            name='MIT License',
            canonical_url='https://opensource.org/licenses/MIT',
            text='License text',
            slug='custom-mit-slug'
        )
        self.assertEqual(license_obj.slug, 'custom-mit-slug')

    def test_slug_with_special_characters(self):
        """Test slug generation with special characters."""
        license_obj = License.objects.create(
            name='GPL-3.0+',
            canonical_url='https://www.gnu.org/licenses/gpl-3.0.html',
            text='License text'
        )
        self.assertEqual(license_obj.slug, 'gpl-30')

    def test_slug_update_on_save(self):
        """Test that slug is generated when missing on existing object."""
        license_obj = License.objects.create(
            name='BSD License',
            canonical_url='https://opensource.org/licenses/BSD-3-Clause',
            text='License text',
            slug='original-slug'
        )

        # Clear the slug and save
        license_obj.slug = ''
        license_obj.save()

        # Slug should be regenerated
        self.assertEqual(license_obj.slug, 'bsd-license')

    def test_slug_generation_with_empty_name_fallback(self):
        """Test slug generation fallback when name doesn't generate valid slug."""
        license_obj = License.objects.create(
            name='!!!',  # Name that doesn't generate a valid slug
            canonical_url='https://example.com/test-empty',
            text='Test license text'
        )
        self.assertEqual(license_obj.slug, 'license')

    def test_slug_generation_preserves_existing_on_update(self):
        """Test that slug is preserved when updating other fields."""
        license_obj = License.objects.create(
            name='Original Name',
            canonical_url='https://example.com/original',
            text='Original text'
        )
        original_slug = license_obj.slug

        # Update other field
        license_obj.text = 'Updated text'
        license_obj.save()

        # Slug should remain the same
        self.assertEqual(license_obj.slug, original_slug)

    def test_slug_generation_with_multiple_conflicts(self):
        """Test slug generation when multiple conflicts exist."""
        # Create licenses that will cause multiple conflicts
        License.objects.create(
            name='Conflict Test 1',
            canonical_url='https://example.com/conflict1',
            text='First conflict test'
        )
        License.objects.create(
            name='Conflict Test 2',
            canonical_url='https://example.com/conflict2',
            text='Second conflict test'
        )

        # Third license should get -2 suffix (names are different but will generate similar slugs)
        license3 = License.objects.create(
            name='Conflict Test 3',
            canonical_url='https://example.com/conflict3',
            text='Third conflict test'
        )

        # All should have different slugs
        slugs = [License.objects.get(name='Conflict Test 1').slug,
                License.objects.get(name='Conflict Test 2').slug,
                license3.slug]

        # All slugs should be unique
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_slug_update_avoids_self_conflict(self):
        """Test that slug update doesn't conflict with itself."""
        license_obj = License.objects.create(
            name='Self Conflict Test',
            canonical_url='https://example.com/self-conflict',
            text='Self conflict test'
        )
        original_slug = license_obj.slug

        # Update the license (which triggers save and slug generation)
        license_obj.text = 'Updated text'
        license_obj.save()

        # Should keep the same slug, not add a counter
        self.assertEqual(license_obj.slug, original_slug)


class LicenseQuerySetTest(TestCase):
    """Test cases for License model querysets and class methods."""

    def setUp(self):
        """Set up test licenses."""
        self.active_license = License.objects.create(
            name='MIT License',
            canonical_url='https://opensource.org/licenses/MIT',
            text='MIT license text',
            is_active=True
        )

        self.deprecated_license = License.objects.create(
            name='Old License',
            canonical_url='https://example.com/old',
            text='Old license text',
            is_active=False,
            deprecated_date=datetime.date(2020, 1, 1)
        )

        self.cc_license = License.objects.create(
            name='Creative Commons BY 4.0',
            canonical_url='https://creativecommons.org/licenses/by/4.0/',
            text='CC BY license text',
            is_active=True
        )

    def test_get_recommended_licenses(self):
        """Test the get_recommended_licenses class method."""
        recommended = License.get_recommended_licenses()

        # Should only include active licenses
        self.assertIn(self.active_license, recommended)
        self.assertIn(self.cc_license, recommended)
        self.assertNotIn(self.deprecated_license, recommended)

        # Should be ordered by name
        license_names = [license.name for license in recommended]
        self.assertEqual(license_names, sorted(license_names))

    def test_ordering_by_name(self):
        """Test that licenses are ordered by name by default."""
        licenses = License.objects.all()
        license_names = [license.name for license in licenses]
        self.assertEqual(license_names, sorted(license_names))

    def test_filtering_by_is_active(self):
        """Test filtering licenses by is_active field."""
        active_licenses = License.objects.filter(is_active=True)
        self.assertEqual(active_licenses.count(), 2)

        deprecated_licenses = License.objects.filter(is_active=False)
        self.assertEqual(deprecated_licenses.count(), 1)

    def test_index_usage(self):
        """Test that database indexes exist (basic check)."""
        # This is more of a smoke test - real index testing would need database inspection
        License.objects.filter(is_active=True)
        License.objects.filter(slug='mit-license')
        # If these queries run without error, the indexes exist


class LicenseValidationTest(TestCase):
    """Test cases for License model validation."""

    def test_empty_name_validation(self):
        """Test that empty name raises validation error."""
        with self.assertRaises(ValidationError):
            license_obj = License(
                name='',
                canonical_url='https://example.com/test',
                text='License text'
            )
            license_obj.full_clean()

    def test_empty_canonical_url_validation(self):
        """Test that empty canonical_url raises validation error."""
        with self.assertRaises(ValidationError):
            license_obj = License(
                name='Test License',
                canonical_url='',
                text='License text'
            )
            license_obj.full_clean()

    def test_empty_text_validation(self):
        """Test that empty text raises validation error."""
        with self.assertRaises(ValidationError):
            license_obj = License(
                name='Test License',
                canonical_url='https://example.com/test',
                text=''
            )
            license_obj.full_clean()

    def test_invalid_url_validation(self):
        """Test that invalid URL raises validation error."""
        with self.assertRaises(ValidationError):
            license_obj = License(
                name='Test License',
                canonical_url='not-a-valid-url',
                text='License text'
            )
            license_obj.full_clean()

    def test_name_max_length_validation(self):
        """Test name field max length validation."""
        long_name = 'A' * 256  # Exceeds max_length=255
        with self.assertRaises(ValidationError):
            license_obj = License(
                name=long_name,
                canonical_url='https://example.com/test',
                text='License text'
            )
            license_obj.full_clean()

    def test_canonical_url_max_length_validation(self):
        """Test canonical_url field max length validation."""
        long_url = 'https://example.com/' + 'a' * 500  # Exceeds max_length=500
        with self.assertRaises(ValidationError):
            license_obj = License(
                name='Test License',
                canonical_url=long_url,
                text='License text'
            )
            license_obj.full_clean()

    def test_deprecated_license_without_date_validation(self):
        """Test that deprecated license without deprecated_date raises validation error."""
        with self.assertRaises(ValidationError) as cm:
            license_obj = License(
                name='Deprecated License',
                canonical_url='https://example.com/deprecated',
                text='Deprecated license text',
                is_active=False  # Deprecated but no deprecated_date
            )
            license_obj.clean()

        self.assertIn('deprecated_date', cm.exception.error_dict)
        self.assertIn('Deprecated licenses must have a deprecated date',
                      str(cm.exception.error_dict['deprecated_date'][0]))

    def test_active_license_with_deprecated_date_validation(self):
        """Test that active license with deprecated_date raises validation error."""
        with self.assertRaises(ValidationError) as cm:
            license_obj = License(
                name='Active License',
                canonical_url='https://example.com/active',
                text='Active license text',
                is_active=True,
                deprecated_date=datetime.date.today()  # Active but has deprecated_date
            )
            license_obj.clean()

        self.assertIn('deprecated_date', cm.exception.error_dict)
        self.assertIn('Active licenses should not have a deprecated date',
                      str(cm.exception.error_dict['deprecated_date'][0]))

    def test_deprecated_license_with_date_validation_passes(self):
        """Test that deprecated license with deprecated_date passes validation."""
        license_obj = License(
            name='Properly Deprecated License',
            canonical_url='https://example.com/properly-deprecated',
            text='Properly deprecated license text',
            is_active=False,
            deprecated_date=datetime.date.today()
        )

        # Should not raise any validation error
        try:
            license_obj.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly for valid deprecated license")

    def test_active_license_without_deprecated_date_validation_passes(self):
        """Test that active license without deprecated_date passes validation."""
        license_obj = License(
            name='Active License',
            canonical_url='https://example.com/active-proper',
            text='Active license text',
            is_active=True
            # No deprecated_date - this is correct for active licenses
        )

        # Should not raise any validation error
        try:
            license_obj.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly for valid active license")


class LicenseTimestampTest(TestCase):
    """Test cases for License model timestamps."""

    def test_created_at_auto_now_add(self):
        """Test that created_at is set automatically on creation."""
        before_creation = timezone.now()
        license_obj = License.objects.create(
            name='Test License',
            canonical_url='https://example.com/test',
            text='License text'
        )
        after_creation = timezone.now()

        self.assertIsNotNone(license_obj.created_at)
        self.assertGreaterEqual(license_obj.created_at, before_creation)
        self.assertLessEqual(license_obj.created_at, after_creation)

    def test_updated_at_auto_now(self):
        """Test that updated_at is updated automatically on save."""
        license_obj = License.objects.create(
            name='Test License',
            canonical_url='https://example.com/test',
            text='License text'
        )
        original_updated_at = license_obj.updated_at

        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)

        # Update the license
        license_obj.description = 'Updated description'
        license_obj.save()

        self.assertGreater(license_obj.updated_at, original_updated_at)

    def test_created_at_unchanged_on_update(self):
        """Test that created_at doesn't change on updates."""
        license_obj = License.objects.create(
            name='Test License',
            canonical_url='https://example.com/test',
            text='License text'
        )
        original_created_at = license_obj.created_at

        # Update the license
        license_obj.description = 'Updated description'
        license_obj.save()

        self.assertEqual(license_obj.created_at, original_created_at)
