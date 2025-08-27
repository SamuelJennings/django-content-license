from django.contrib import admin
from django.template.defaultfilters import linebreaks
from django.utils.html import mark_safe
from django.utils.translation import gettext as _

from licensing.models import License

from .models import TestModel


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = [
        # "name",
        "license",
        # "get_license_display",
    ]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
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
        return mark_safe(f"<nobr>{obj.name}</nobr>")

    get_name_display.short_description = _("name")

    def get_canonical_url_display(self, obj):
        return mark_safe(f'<a href="{obj.canonical_url}" target="_blank">{obj.canonical_url}</a>')

    get_canonical_url_display.short_description = _("canonical URL")

    def get_description_display(self, obj):
        if obj.description:
            return mark_safe(linebreaks(obj.description))
        return _("No description")

    get_description_display.short_description = _("description")
