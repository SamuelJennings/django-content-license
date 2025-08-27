"""
Utility functions for django-content-license package.
"""
import logging

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def get_license_attribution(model_instance):
    """
    Get attribution information for a model instance.
    
    Args:
        model_instance: Django model instance
        
    Returns:
        dict: Attribution information with keys:
            - title: String representation of the instance
            - link: URL to the instance (if available)
            - creators: Creator information or "Unknown"
            - creators_link: URL to the creators (if available)
    """
    try:
        attr = {
            "title": str(model_instance),
            "link": getattr(model_instance, 'get_absolute_url', lambda: None)(),
            "creators": getattr(model_instance, 'creators', None) or _("Unknown"),
            "creators_link": None,
        }

        # Try to get creators link if creators exist
        if hasattr(model_instance, 'creators') and model_instance.creators:
            try:
                creators_link = getattr(model_instance.creators, 'get_absolute_url', lambda: None)()
                attr["creators_link"] = creators_link
            except AttributeError:
                # Creator has no URL - this is fine, just leave creators_link as None
                pass

        return attr
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


def get_license_creator(model_instance):
    """
    Get the creator of a model instance.
    
    Args:
        model_instance: Django model instance
        
    Returns:
        Creator object or None if no creator attribute exists
    """
    return getattr(model_instance, 'creator', None)


def html_snippet(model_instance, field_name):
    """
    Generate HTML snippet for license attribution.
    
    Args:
        model_instance: Django model instance
        field_name: Name of the license field
        
    Returns:
        str: HTML snippet for license attribution or empty string if error/no license
    """
    try:
        license_obj = getattr(model_instance, field_name, None)
        if not license_obj:
            return ""

        snippet = render_to_string(
            "licensing/snippet.html",
            {"object": model_instance, "license": license_obj}
        )
        return mark_safe(snippet)  # noqa: S308
    except Exception as e:
        logger.warning(f"Error generating license snippet: {e}")
        return ""


def get_attribution_context(model_instance, license_obj):
    """
    Get context dictionary for license attribution template.
    
    Args:
        model_instance: Django model instance
        license_obj: License instance
        
    Returns:
        dict: Context for template rendering
    """
    attribution = get_license_attribution(model_instance)
    return {
        "object": model_instance,
        "license": license_obj,
        "attribution": attribution,
    }


def validate_license_field_name(model_class, field_name):
    """
    Validate that a field name exists on a model and is a license field.
    
    Args:
        model_class: Django model class
        field_name: Name of the field to validate
        
    Returns:
        bool: True if field exists and is valid
        
    Raises:
        AttributeError: If field doesn't exist
        ValueError: If field is not a license field
    """
    if not hasattr(model_class, field_name):
        raise AttributeError(f"Model {model_class.__name__} has no field '{field_name}'")

    field = model_class._meta.get_field(field_name)
    if not hasattr(field, 'remote_field') or not field.remote_field:
        raise ValueError(f"Field '{field_name}' is not a foreign key field")

    related_model = field.remote_field.model
    if isinstance(related_model, str):
        return related_model == 'licensing.License'
    else:
        return related_model.__name__ == 'License'
