# SPDX-License-Identifier: MIT

from django.contrib import admin
from .models import License


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ["spdx", "name", "short_name", "description"]
    search_fields = ["name", "spdx"]

    readonly_fields = ["html", "template"]
