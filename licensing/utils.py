"""Attribution helpers and license-field validation."""

import logging

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class LicenseFieldError(Exception):
    """Base exception for license field validation errors."""


class LicenseFieldNotFoundError(LicenseFieldError):
    """Raised when a license field is not found on a model.

    Args:
        model_name: Name of the model that was searched.
        field_name: Name of the field that was not found.
    """

    def __init__(self, model_name, field_name):
        super().__init__(f"Model {model_name} has no field '{field_name}'")
        self.model_name = model_name
        self.field_name = field_name


class InvalidLicenseFieldError(LicenseFieldError):
    """Raised when a field is not a valid license field.

    Args:
        field_name: Name of the rejected field.
        reason: Why the field is not a license field.
    """

    def __init__(self, field_name, reason):
        super().__init__(f"Field '{field_name}' is not a valid license field: {reason}")
        self.field_name = field_name
        self.reason = reason


def get_license_attribution(model_instance):
    """Return attribution information for a model instance.

    Args:
        model_instance: The instance being attributed.

    Returns:
        A dict with `title` (the instance as a string), `link` (its URL, or None),
        `creators` (its `creators`, or "Unknown") and `creators_link` (the creators'
        URL, or None). Any error while reading the instance yields the fallback values.
    """
    try:
        attr = {
            "title": str(model_instance),
            "link": getattr(model_instance, "get_absolute_url", lambda: None)(),
            "creators": getattr(model_instance, "creators", None) or _("Unknown"),
            "creators_link": None,
        }

        if hasattr(model_instance, "creators") and model_instance.creators:
            try:
                creators_link = getattr(
                    model_instance.creators, "get_absolute_url", lambda: None
                )()
            except AttributeError:
                creators_link = None
            else:
                attr["creators_link"] = creators_link

    except Exception as e:
        try:
            instance_str = str(model_instance)
        except Exception:
            instance_str = f"<{type(model_instance).__name__} object>"

        logger.warning(f"Error getting license attribution for {instance_str}: {e}")
        return {
            "title": instance_str,
            "link": None,
            "creators": _("Unknown"),
            "creators_link": None,
        }
    else:
        return attr


def get_license_creator(model_instance):
    """Return the creator of a model instance.

    Args:
        model_instance: The instance to read `creator` from.

    Returns:
        The instance's `creator`, or None when it has none.
    """
    return getattr(model_instance, "creator", None)


def html_snippet(model_instance, field_name):
    """Render the attribution snippet for a model instance.

    Args:
        model_instance: The instance being attributed.
        field_name: Name of its license field.

    Returns:
        The rendered `licensing/snippet.html`, or an empty string when the instance has
        no license or rendering fails.
    """
    try:
        license_obj = getattr(model_instance, field_name, None)
        if not license_obj:
            return ""

        snippet = render_to_string(
            "licensing/snippet.html", {"object": model_instance, "license": license_obj}
        )
        return mark_safe(snippet)
    except Exception as e:
        logger.warning(f"Error generating license snippet: {e}")
        return ""


def get_attribution_context(model_instance, license_obj):
    """Return the template context for rendering an attribution.

    Args:
        model_instance: The instance being attributed.
        license_obj: The license it is published under.

    Returns:
        A dict with `object`, `license` and `attribution` (see `get_license_attribution`).
    """
    attribution = get_license_attribution(model_instance)
    return {
        "object": model_instance,
        "license": license_obj,
        "attribution": attribution,
    }


def validate_license_field_name(model_class, field_name):
    """Check that a field exists on a model and is a license field.

    Args:
        model_class: The model class to inspect.
        field_name: Name of the field to check.

    Returns:
        True when the field is a foreign key to `License`, False when it points elsewhere.

    Raises:
        LicenseFieldNotFoundError: The model has no such field.
        InvalidLicenseFieldError: The field is not a foreign key.
    """
    if not hasattr(model_class, field_name):
        raise LicenseFieldNotFoundError(model_class.__name__, field_name)

    field = model_class._meta.get_field(field_name)
    if not hasattr(field, "remote_field") or not field.remote_field:
        raise InvalidLicenseFieldError(field_name, "not a foreign key field")

    related_model = field.remote_field.model
    if isinstance(related_model, str):
        return related_model == "licensing.License"
    else:
        return related_model.__name__ == "License"
