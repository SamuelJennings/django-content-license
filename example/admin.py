"""Admin for the example project and the License model."""

from django.contrib import admin
from django.template.defaultfilters import linebreaks
from django.utils.html import mark_safe
from django.utils.translation import gettext as _

from licensing.models import License

from .models import TestModel


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    """List example content with its license."""

    list_display = [
        "content_license",
    ]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    """List, filter and search licenses."""

    list_display = [
        "get_name_display",
        "get_canonical_url_display",
        "get_description_display",
        "status_display",
    ]
    list_filter = ["is_active", "deprecated_date"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at", "slug"]

    def get_name_display(self, obj):
        """Return the name, kept on one line.

        Args:
            obj: The license being listed.

        Returns:
            The name wrapped in `<nobr>`.
        """
        return mark_safe(f"<nobr>{obj.name}</nobr>")

    get_name_display.short_description = _("name")

    def get_canonical_url_display(self, obj):
        """Return the canonical URL as a link that opens in a new tab.

        Args:
            obj: The license being listed.

        Returns:
            An anchor pointing at the canonical URL.
        """
        return mark_safe(
            f'<a href="{obj.canonical_url}" target="_blank">{obj.canonical_url}</a>'
        )

    get_canonical_url_display.short_description = _("canonical URL")

    def get_description_display(self, obj):
        """Return the description as paragraphs, or a placeholder when empty.

        Args:
            obj: The license being listed.

        Returns:
            The description with line breaks rendered as HTML.
        """
        if obj.description:
            return mark_safe(linebreaks(obj.description))
        return _("No description")

    get_description_display.short_description = _("description")
