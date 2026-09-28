"""Tests for the utility functions in django-content-license."""

import logging
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
    def test_full_data(self):
        creator = MockCreator()
        model_instance = MockModel(creators=creator)

        result = get_license_attribution(model_instance)

        assert result["title"] == "Test Object"
        assert result["link"] == "/object/1/"
        assert result["creators"] == creator
        assert result["creators_link"] == "/creator/1/"

    def test_no_creators(self):
        model_instance = MockModel()

        result = get_license_attribution(model_instance)

        assert result["title"] == "Test Object"
        assert result["link"] == "/object/1/"
        assert "Unknown" in str(result["creators"])
        assert result["creators_link"] is None

    def test_no_url(self):
        model_instance = MockModel(has_url=False)

        result = get_license_attribution(model_instance)

        assert result["title"] == "Test Object"
        assert result["link"] is None
        assert "Unknown" in str(result["creators"])
        assert result["creators_link"] is None

    def test_creators_no_url(self):
        creator = MockCreator(has_url=False)
        model_instance = MockModel(creators=creator)

        result = get_license_attribution(model_instance)

        assert result["title"] == "Test Object"
        assert result["link"] == "/object/1/"
        assert result["creators"] == creator
        assert result["creators_link"] is None

    def test_exception_handling(self):
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Test error"))

        result = get_license_attribution(model_instance)

        assert "Unknown" in str(result["creators"])
        assert result["link"] is None
        assert result["creators_link"] is None

    def test_str_exception(self):
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Conversion error"))

        result = get_license_attribution(model_instance)

        assert "Mock" in result["title"]
        assert result["link"] is None
        assert "Unknown" in str(result["creators"])
        assert result["creators_link"] is None

    def test_logs_error(self, caplog):
        model_instance = Mock()
        model_instance.__str__ = Mock(side_effect=Exception("Test error"))

        get_license_attribution(model_instance)

        assert [r.levelno for r in caplog.records] == [logging.WARNING]

    def test_empty_creators(self):
        model_instance = MockModel()
        model_instance.creators = ""

        result = get_license_attribution(model_instance)

        assert "Unknown" in str(result["creators"])

    def test_falsy_creators(self):
        model_instance = MockModel()
        model_instance.creators = 0

        result = get_license_attribution(model_instance)

        assert "Unknown" in str(result["creators"])


class TestGetLicenseCreator:
    def test_with_creator(self):
        creator = "Test Creator"
        model_instance = MockModel(creator=creator)

        result = get_license_creator(model_instance)

        assert result == creator

    def test_no_creator(self):
        model_instance = MockModel()

        result = get_license_creator(model_instance)

        assert result is None

    def test_with_object_creator(self):
        creator_obj = MockCreator()
        model_instance = MockModel(creator=creator_obj)

        result = get_license_creator(model_instance)

        assert result == creator_obj


class TestHtmlSnippet:
    @patch("licensing.utils.render_to_string")
    def test_success(self, mock_render, license_obj):
        mock_render.return_value = "<div>License snippet</div>"

        model_instance = MockModel()
        model_instance.test_license = license_obj

        result = html_snippet(model_instance, "test_license")

        mock_render.assert_called_once_with(
            "licensing/snippet.html", {"object": model_instance, "license": license_obj}
        )
        assert "<div>License snippet</div>" in result

    def test_no_license(self):
        model_instance = MockModel()
        model_instance.test_license = None

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    def test_missing_field(self):
        model_instance = MockModel()

        result = html_snippet(model_instance, "nonexistent_field")

        assert result == ""

    @patch("licensing.utils.render_to_string")
    def test_template_error(self, mock_render, license_obj):
        mock_render.side_effect = TemplateDoesNotExist("snippet.html")

        model_instance = MockModel()
        model_instance.test_license = license_obj

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    @patch("licensing.utils.render_to_string")
    def test_general_exception(self, mock_render, license_obj):
        mock_render.side_effect = Exception("Unexpected error")

        model_instance = MockModel()
        model_instance.test_license = license_obj

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    @patch("licensing.utils.render_to_string")
    def test_logs_error(self, mock_render, caplog):
        mock_render.side_effect = Exception("Template error")

        model_instance = MockModel()
        model_instance.test_license = Mock()

        html_snippet(model_instance, "test_license")

        assert [r.levelno for r in caplog.records] == [logging.WARNING]

    def test_with_none_attribute(self):
        model_instance = MockModel()

        result = html_snippet(model_instance, "test_license")

        assert result == ""

    def test_with_false_license(self):
        model_instance = MockModel()
        model_instance.test_license = False

        result = html_snippet(model_instance, "test_license")

        assert result == ""


class TestGetAttributionContext:
    def test_basic(self, license_obj):
        model_instance = MockModel()

        result = get_attribution_context(model_instance, license_obj)

        assert result["object"] == model_instance
        assert result["license"] == license_obj
        assert "attribution" in result
        assert result["attribution"]["title"] == "Test Object"

    def test_with_creators(self, license_obj):
        creator = MockCreator()
        model_instance = MockModel(creators=creator)

        result = get_attribution_context(model_instance, license_obj)

        assert result["object"] == model_instance
        assert result["license"] == license_obj
        assert result["attribution"]["creators"] == creator
        assert result["attribution"]["creators_link"] == "/creator/1/"


class TestValidateLicenseFieldName:
    def test_valid_field(self):
        class ValidFieldModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(ValidFieldModel, "license")

        assert result is True

    def test_string_model_reference(self):
        class StringRefModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(StringRefModel, "license")

        assert result is True

    def test_string_model_reference_wrong_model(self):
        class WrongStringRefModel(models.Model):
            user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(WrongStringRefModel, "user")

        assert result is False

    def test_missing_field(self):
        class MissingFieldModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = "test"

        with pytest.raises(LicenseFieldNotFoundError) as exc_info:
            validate_license_field_name(MissingFieldModel, "nonexistent")

        assert exc_info.value.model_name == "MissingFieldModel"
        assert exc_info.value.field_name == "nonexistent"

    def test_non_foreign_key(self):
        class NonForeignKeyModel(models.Model):
            license = models.ForeignKey("licensing.License", on_delete=models.CASCADE)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = "test"

        with pytest.raises(InvalidLicenseFieldError) as exc_info:
            validate_license_field_name(NonForeignKeyModel, "name")

        assert exc_info.value.field_name == "name"

    def test_wrong_model(self):
        class WrongUtilsModel(models.Model):
            other = models.ForeignKey("auth.User", on_delete=models.CASCADE)

            class Meta:
                app_label = "test"

        result = validate_license_field_name(WrongUtilsModel, "other")

        assert result is False
