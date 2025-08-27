"""
Tests for the utility functions in django-content-license.
"""
from unittest.mock import Mock, patch

from django.db import models
from django.template import TemplateDoesNotExist
from django.test import TestCase

from licensing.models import License
from licensing.utils import (
    get_attribution_context,
    get_license_attribution,
    get_license_creator,
    html_snippet,
    validate_license_field_name,
)


class MockCreator:
    """Mock creator object for testing."""

    def __init__(self, name="Test Creator", has_url=True):
        self.name = name
        self._has_url = has_url

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self._has_url:
            return "/creator/1/"
        raise AttributeError("Mock creator has no URL")


class MockModel:
    """Mock model for testing utility functions."""

    def __init__(self, name="Test Object", has_url=True, creators=None, creator=None):
        self.name = name
        self._has_url = has_url
        self.creators = creators
        self.creator = creator

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self._has_url:
            return "/object/1/"
        raise AttributeError("Mock object has no URL")


class GetLicenseAttributionTest(TestCase):
    """Test cases for get_license_attribution function."""

    def test_get_license_attribution_full_data(self):
        """Test get_license_attribution with full data."""
        creator = MockCreator()
        model_instance = MockModel(creators=creator)

        result = get_license_attribution(model_instance)

        self.assertEqual(result['title'], 'Test Object')
        self.assertEqual(result['link'], '/object/1/')
        self.assertEqual(result['creators'], creator)
        self.assertEqual(result['creators_link'], '/creator/1/')

    def test_get_license_attribution_no_creators(self):
        """Test get_license_attribution without creators."""
        model_instance = MockModel()

        result = get_license_attribution(model_instance)

        self.assertEqual(result['title'], 'Test Object')
        self.assertEqual(result['link'], '/object/1/')
        self.assertIn('Unknown', str(result['creators']))
        self.assertIsNone(result['creators_link'])

    def test_get_license_attribution_no_url(self):
        """Test get_license_attribution without URL."""
        model_instance = MockModel(has_url=False)

        result = get_license_attribution(model_instance)

        self.assertEqual(result['title'], 'Test Object')
        self.assertIsNone(result['link'])
        self.assertIn('Unknown', str(result['creators']))
        self.assertIsNone(result['creators_link'])

    def test_get_license_attribution_creators_no_url(self):
        """Test get_license_attribution with creators but no URL."""
        creator = MockCreator(has_url=False)
        model_instance = MockModel(creators=creator)

        result = get_license_attribution(model_instance)

        # The function should succeed even if creator.get_absolute_url() raises an exception
        self.assertEqual(result['title'], 'Test Object')
        self.assertEqual(result['link'], '/object/1/')
        self.assertEqual(result['creators'], creator)
        self.assertIsNone(result['creators_link'])  # Should be None because creator has no URL

    def test_get_license_attribution_exception_handling(self):
        """Test get_license_attribution exception handling."""
        # Create a mock that raises an exception
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Test error"))

        result = get_license_attribution(model_instance)

        # Should return fallback values
        self.assertIn('Unknown', str(result['creators']))
        self.assertIsNone(result['link'])
        self.assertIsNone(result['creators_link'])

    def test_get_license_attribution_str_exception(self):
        """Test handling when str() raises exception."""
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Conversion error"))

        result = get_license_attribution(model_instance)

        # Should have fallback values - title should be the fallback representation
        self.assertIn('Mock', result['title'])  # Should use the fallback format
        self.assertIsNone(result['link'])
        self.assertIn('Unknown', str(result['creators']))
        self.assertIsNone(result['creators_link'])


class GetLicenseCreatorTest(TestCase):
    """Test cases for get_license_creator function."""

    def test_get_license_creator_with_creator(self):
        """Test get_license_creator when creator exists."""
        creator = "Test Creator"
        model_instance = MockModel(creator=creator)

        result = get_license_creator(model_instance)

        self.assertEqual(result, creator)

    def test_get_license_creator_no_creator(self):
        """Test get_license_creator when no creator exists."""
        model_instance = MockModel()

        result = get_license_creator(model_instance)

        self.assertIsNone(result)

    def test_get_license_creator_with_object_creator(self):
        """Test get_license_creator with object creator."""
        creator_obj = MockCreator()
        model_instance = MockModel(creator=creator_obj)

        result = get_license_creator(model_instance)

        self.assertEqual(result, creator_obj)


class HtmlSnippetTest(TestCase):
    """Test cases for html_snippet function."""

    def setUp(self):
        """Set up test data."""
        self.license = License.objects.create(
            name='Test License',
            canonical_url='https://example.com/license',
            description='A test license',
            text='This is the full license text.'
        )

    @patch('licensing.utils.render_to_string')
    def test_html_snippet_success(self, mock_render):
        """Test html_snippet function success case."""
        mock_render.return_value = "<div>License snippet</div>"

        model_instance = MockModel()
        model_instance.test_license = self.license

        result = html_snippet(model_instance, 'test_license')

        mock_render.assert_called_once_with(
            "licensing/snippet.html",
            {"object": model_instance, "license": self.license}
        )
        self.assertIn("<div>License snippet</div>", result)

    def test_html_snippet_no_license(self):
        """Test html_snippet when license is None."""
        model_instance = MockModel()
        model_instance.test_license = None

        result = html_snippet(model_instance, 'test_license')

        self.assertEqual(result, "")

    def test_html_snippet_missing_field(self):
        """Test html_snippet when field doesn't exist."""
        model_instance = MockModel()

        result = html_snippet(model_instance, 'nonexistent_field')

        self.assertEqual(result, "")

    @patch('licensing.utils.render_to_string')
    def test_html_snippet_template_error(self, mock_render):
        """Test html_snippet template rendering error."""
        mock_render.side_effect = TemplateDoesNotExist("snippet.html")

        model_instance = MockModel()
        model_instance.test_license = self.license

        result = html_snippet(model_instance, 'test_license')

        self.assertEqual(result, "")

    @patch('licensing.utils.render_to_string')
    def test_html_snippet_general_exception(self, mock_render):
        """Test html_snippet general exception handling."""
        mock_render.side_effect = Exception("Unexpected error")

        model_instance = MockModel()
        model_instance.test_license = self.license

        result = html_snippet(model_instance, 'test_license')

        self.assertEqual(result, "")


class GetAttributionContextTest(TestCase):
    """Test cases for get_attribution_context function."""

    def setUp(self):
        """Set up test data."""
        self.license = License.objects.create(
            name='Test License',
            canonical_url='https://example.com/license',
            description='A test license',
            text='This is the full license text.'
        )

    def test_get_attribution_context_basic(self):
        """Test get_attribution_context with basic data."""
        model_instance = MockModel()

        result = get_attribution_context(model_instance, self.license)

        self.assertEqual(result['object'], model_instance)
        self.assertEqual(result['license'], self.license)
        self.assertIn('attribution', result)
        self.assertEqual(result['attribution']['title'], 'Test Object')

    def test_get_attribution_context_with_creators(self):
        """Test get_attribution_context with creators."""
        creator = MockCreator()
        model_instance = MockModel(creators=creator)

        result = get_attribution_context(model_instance, self.license)

        self.assertEqual(result['object'], model_instance)
        self.assertEqual(result['license'], self.license)
        self.assertEqual(result['attribution']['creators'], creator)
        self.assertEqual(result['attribution']['creators_link'], '/creator/1/')


class ValidateLicenseFieldNameTest(TestCase):
    """Test cases for validate_license_field_name function."""

    def setUp(self):
        """Set up test models."""
        # Create a test model class
        class UtilsTestModel(models.Model):
            license = models.ForeignKey('licensing.License', on_delete=models.CASCADE)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = 'test'

        self.UtilsTestModel = UtilsTestModel

    def test_validate_license_field_name_valid_field(self):
        """Test validation with valid license field."""
        result = validate_license_field_name(self.UtilsTestModel, 'license')

        self.assertTrue(result)

    def test_validate_license_field_name_string_model_reference(self):
        """Test validation with string model reference (covers untested branch)."""
        # Create a model with string reference to License model
        class StringRefModel(models.Model):
            license = models.ForeignKey('licensing.License', on_delete=models.CASCADE)

            class Meta:
                app_label = 'test'

        result = validate_license_field_name(StringRefModel, 'license')

        # This should return True for string reference to 'licensing.License'
        self.assertTrue(result)

    def test_validate_license_field_name_string_model_reference_wrong_model(self):
        """Test validation with string reference to wrong model."""
        # Create a model with string reference to different model
        class WrongStringRefModel(models.Model):
            user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

            class Meta:
                app_label = 'test'

        result = validate_license_field_name(WrongStringRefModel, 'user')

        # This should return False for string reference to non-License model
        self.assertFalse(result)

    def test_validate_license_field_name_missing_field(self):
        """Test validation with missing field."""
        from licensing.utils import LicenseFieldNotFoundError

        with self.assertRaises(LicenseFieldNotFoundError) as cm:
            validate_license_field_name(self.UtilsTestModel, 'nonexistent')

        self.assertIn("has no field 'nonexistent'", str(cm.exception))

    def test_validate_license_field_name_non_foreign_key(self):
        """Test validation with non-foreign key field."""
        from licensing.utils import InvalidLicenseFieldError

        with self.assertRaises(InvalidLicenseFieldError) as cm:
            validate_license_field_name(self.UtilsTestModel, 'name')

        self.assertIn("is not a valid license field", str(cm.exception))

    def test_validate_license_field_name_wrong_model(self):
        """Test validation with foreign key to wrong model."""
        # Create a test model with foreign key to different model
        class WrongUtilsModel(models.Model):
            other = models.ForeignKey('auth.User', on_delete=models.CASCADE)

            class Meta:
                app_label = 'test'

        result = validate_license_field_name(WrongUtilsModel, 'other')

        self.assertFalse(result)


class UtilsLoggingTest(TestCase):
    """Test cases for logging in utility functions."""

    @patch('licensing.utils.logger')
    def test_get_license_attribution_logs_error(self, mock_logger):
        """Test that get_license_attribution logs errors."""
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Test error"))

        get_license_attribution(model_instance)

        mock_logger.warning.assert_called_once()
        self.assertIn("Error getting license attribution", mock_logger.warning.call_args[0][0])

    @patch('licensing.utils.logger')
    @patch('licensing.utils.render_to_string')
    def test_html_snippet_logs_error(self, mock_render, mock_logger):
        """Test that html_snippet logs errors."""
        mock_render.side_effect = Exception("Template error")

        model_instance = MockModel()
        model_instance.test_license = Mock()

        html_snippet(model_instance, 'test_license')

        mock_logger.warning.assert_called_once()
        self.assertIn("Error generating license snippet", mock_logger.warning.call_args[0][0])


class UtilsEdgeCasesTest(TestCase):
    """Test edge cases for utility functions."""

    def test_get_license_attribution_empty_creators(self):
        """Test get_license_attribution with empty creators."""
        model_instance = MockModel()
        model_instance.creators = ""  # Empty string

        result = get_license_attribution(model_instance)

        self.assertIn('Unknown', str(result['creators']))

    def test_get_license_attribution_falsy_creators(self):
        """Test get_license_attribution with falsy creators."""
        model_instance = MockModel()
        model_instance.creators = 0  # Falsy value

        result = get_license_attribution(model_instance)

        self.assertIn('Unknown', str(result['creators']))

    def test_html_snippet_with_none_attribute(self):
        """Test html_snippet when getattr returns None."""
        model_instance = MockModel()
        # Don't set test_license attribute

        result = html_snippet(model_instance, 'test_license')

        self.assertEqual(result, "")

    def test_html_snippet_with_false_license(self):
        """Test html_snippet when license field is falsy."""
        model_instance = MockModel()
        model_instance.test_license = False

        result = html_snippet(model_instance, 'test_license')

        self.assertEqual(result, "")
