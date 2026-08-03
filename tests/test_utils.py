"""
Tests for the utility functions in django-content-license.
"""

from unittest.mock import Mock, patch

import pytest
from django.db import models
from django.template import TemplateDoesNotExist

from licensing.utils import (
    InvalidLicenseFieldError,
    LicenseFieldNotFoundError,
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


class TestGetLicenseAttribution:
    """Test cases for get_license_attribution function."""

    def test_full_data(self):
        """Test get_license_attribution with full data."""
        creator = MockCreator()
        model_instance = MockModel(creators=creator)

        result = get_license_attribution(model_instance)

        assert result["title"] == "Test Object"
        assert result["link"] == "/object/1/"
        assert result["creators"] == creator
        assert result["creators_link"] == "/creator/1/"

    def test_no_creators(self):
        """Test get_license_attribution without creators."""
        model_instance = MockModel()

        result = get_license_attribution(model_instance)

        assert result["title"] == "Test Object"
        assert result["link"] == "/object/1/"
        assert "Unknown" in str(result["creators"])
        assert result["creators_link"] is None

    def test_no_url(self):
        """Test get_license_attribution without URL."""
        model_instance = MockModel(has_url=False)

        result = get_license_attribution(model_instance)

        assert result["title"] == "Test Object"
        assert result["link"] is None
        assert "Unknown" in str(result["creators"])
        assert result["creators_link"] is None

    def test_creators_no_url(self):
        """Test get_license_attribution with creators but no URL."""
        creator = MockCreator(has_url=False)
        model_instance = MockModel(creators=creator)

        result = get_license_attribution(model_instance)

        # The function should succeed even if creator.get_absolute_url() raises an exception
        assert result["title"] == "Test Object"
        assert result["link"] == "/object/1/"
        assert result["creators"] == creator
        assert result["creators_link"] is None  # Should be None because creator has no URL

    def test_exception_handling(self):
        """Test get_license_attribution exception handling."""
        # Create a mock that raises an exception
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Test error"))

        result = get_license_attribution(model_instance)

        # Should return fallback values
        assert "Unknown" in str(result["creators"])
        assert result["link"] is None
        assert result["creators_link"] is None

    def test_str_exception(self):
        """Test handling when str() raises exception."""
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Conversion error"))

        result = get_license_attribution(model_instance)

        # Should have fallback values - title should be the fallback representation
        assert "Mock" in result["title"]  # Should use the fallback format
        assert result["link"] is None
        assert "Unknown" in str(result["creators"])
        assert result["creators_link"] is None

    @patch("licensing.utils.logger")
    def test_logs_error(self, mock_logger):
        """Test that get_license_attribution logs errors."""
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Test error"))

        get_license_attribution(model_instance)

        mock_logger.warning.assert_called_once()
        assert "Error getting license attribution" in mock_logger.warning.call_args[0][0]

    def test_empty_creators(self):
        """Test get_license_attribution with empty creators."""
        model_instance = MockModel()
        model_instance.creators = ""  # Empty string

        result = get_license_attribution(model_instance)

        assert "Unknown" in str(result["creators"])

    def test_falsy_creators(self):
        """Test get_license_attribution with falsy creators."""
        model_instance = MockModel()
        model_instance.creators = 0  # Falsy value

        result = get_license_attribution(model_instance)

        assert "Unknown" in str(result["creators"])


class TestGetLicenseCreator:
    """Test cases for get_license_creator function."""

    def test_with_creator(self):
        """Test get_license_creator when creator exists."""
        creator = "Test Creator"
        model_instance = MockModel(creator=creator)

        result = get_license_creator(model_instance)

        assert result == creator

    def test_no_creator(self):
        """Test get_license_creator when no creator exists."""
        model_instance = MockModel()

        result = get_license_creator(model_instance)

        assert result is None

    def test_with_object_creator(self):
        """Test get_license_creator with object creator."""
        creator_obj = MockCreator()
        model_instance = MockModel(creator=creator_obj)

        result = get_license_creator(model_instance)

        assert result == creator_obj


class TestHtmlSnippet:
    """Test cases for html_snippet function."""

    @patch("licensing.utils.render_to_string")
    def test_success(self, mock_render, license_obj):
        """Test html_snippet function success case."""
        mock_render.return_value = "<div>License snippet</div>"

        model_instance = MockModel()
        model_instance.test_license = license_obj

        result = html_snippet(model_instance, "test_license")

        mock_render.assert_called_once_with(
            "licensing/snippet.html", {"object": model_instance, "license": license_obj}
        )
        assert "<div>License snippet</div>" in result

    def test_no_license(self):
        """Test html_snippet when license is None."""
        model_instance = MockModel()
        model_instance.test_license = None

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    def test_missing_field(self):
        """Test html_snippet when field doesn't exist."""
        model_instance = MockModel()

        result = html_snippet(model_instance, "nonexistent_field")

        assert result == ""

    @patch("licensing.utils.render_to_string")
    def test_template_error(self, mock_render, license_obj):
        """Test html_snippet template rendering error."""
        mock_render.side_effect = TemplateDoesNotExist("snippet.html")

        model_instance = MockModel()
        model_instance.test_license = license_obj

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    @patch("licensing.utils.render_to_string")
    def test_general_exception(self, mock_render, license_obj):
        """Test html_snippet general exception handling."""
        mock_render.side_effect = Exception("Unexpected error")

        model_instance = MockModel()
        model_instance.test_license = license_obj

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    @patch("licensing.utils.logger")
    @patch("licensing.utils.render_to_string")
    def test_logs_error(self, mock_render, mock_logger):
        """Test that html_snippet logs errors."""
        mock_render.side_effect = Exception("Template error")

        model_instance = MockModel()
        model_instance.test_license = Mock()

        html_snippet(model_instance, "test_license")

        mock_logger.warning.assert_called_once()
        assert "Error generating license snippet" in mock_logger.warning.call_args[0][0]

    def test_with_none_attribute(self):
        """Test html_snippet when getattr returns None."""
        model_instance = MockModel()
        # Don't set test_license attribute

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    def test_with_false_license(self):
        """Test html_snippet when license field is falsy."""
        model_instance = MockModel()
        model_instance.test_license = False

        result = html_snippet(model_instance, "test_license")

        assert result == ""


class TestGetAttributionContext:
    """Test cases for get_attribution_context function."""

    def test_basic(self, license_obj):
        """Test get_attribution_context with basic data."""
        model_instance = MockModel()

        result = get_attribution_context(model_instance, license_obj)

        assert result["object"] == model_instance
        assert result["license"] == license_obj
        assert "attribution" in result
        assert result["attribution"]["title"] == "Test Object"

    def test_with_creators(self, license_obj):
        """Test get_attribution_context with creators."""
        creator = MockCreator()
        model_instance = MockModel(creators=creator)

        result = get_attribution_context(model_instance, license_obj)

        assert result["object"] == model_instance
        assert result["license"] == license_obj
        assert result["attribution"]["creators"] == creator
        assert result["attribution"]["creators_link"] == "/creator/1/"


class TestValidateLicenseFieldName:
    """Test cases for validate_license_field_name function."""

    def test_valid_field(self):
        """Test validation with valid license field."""

        class UtilsTestModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(UtilsTestModel, "license")

        assert result is True

    def test_string_model_reference(self):
        """Test validation with string model reference (covers untested branch)."""

        # Create a model with string reference to License model
        class StringRefModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(StringRefModel, "license")

        # This should return True for string reference to 'licensing.License'
        assert result is True

    def test_string_model_reference_wrong_model(self):
        """Test validation with string reference to wrong model."""

        # Create a model with string reference to different model
        class WrongStringRefModel(models.Model):
            user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(WrongStringRefModel, "user")

        # This should return False for string reference to non-License model
        assert result is False

    def test_missing_field(self):
        """Test validation with missing field."""

        class UtilsTestModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = "test"

        with pytest.raises(LicenseFieldNotFoundError) as exc_info:
            validate_license_field_name(UtilsTestModel, "nonexistent")

        assert "has no field 'nonexistent'" in str(exc_info.value)

    def test_non_foreign_key(self):
        """Test validation with non-foreign key field."""

        class UtilsTestModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = "test"

        with pytest.raises(InvalidLicenseFieldError) as exc_info:
            validate_license_field_name(UtilsTestModel, "name")

        assert "is not a valid license field" in str(exc_info.value)

    def test_wrong_model(self):
        """Test validation with foreign key to wrong model."""

        # Create a test model with foreign key to different model
        class WrongUtilsModel(models.Model):
            other = models.ForeignKey("auth.User", on_delete=models.CASCADE)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(WrongUtilsModel, "other")

        assert result is False
