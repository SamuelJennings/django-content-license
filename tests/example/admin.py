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
        "get_URL_display",
        "get_description_display",
    ]

    def get_name_display(self, obj):
        return mark_safe(f"<nobr>{obj.name}</nobr>")

    get_name_display.short_description = _("name")

    def get_URL_display(self, obj):
        return mark_safe(f'<a href="{obj.URL}">{obj.URL}</a>')

    get_URL_display.short_description = _("URL")

    def get_description_display(self, obj):
        return mark_safe(linebreaks(obj.description))

    get_description_display.short_description = _("description")
