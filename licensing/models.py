import requests
from django.db import models
from django.utils.translation import gettext_lazy as _
from requests.exceptions import ConnectionError


def get_licenses():
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json"
        )
    except ConnectionError:
        return {}
    data = response.json()
    licenses = {lic["licenseId"]: lic["name"] for lic in data["licenses"]}
    return licenses


class License(models.Model):
    # SPDX_LICENCES = get_licenses()
    name = models.CharField(
        _("name"),
        help_text=_(
            "The full name of the license as specified by https://spdx.org/licenses/"
        ),
        max_length=255,
    )
    description = models.TextField(
        _("description"),
        help_text=_("A human-readable description of the license."),
        null=True,
        blank=True,
    )

    short_name = models.CharField(
        _("short name"),
        max_length=255,
        help_text=_("Customary short name if applicable (e.g, GPLv3)"),
        null=True,
        blank=True,
    )

    recommended = models.BooleanField(
        _("recommended"),
        help_text=_(
            "Whether the license is recommended for items in this dataset. Recommended items will show first in select boxes"
        ),
        default=False,
    )
    hidden = models.BooleanField(
        _("hidden"),
        help_text=_(
            "Licenses marked as hidden are allowed in the database but cannot be selected for new projects."
        ),
        default=True,
    )

    spdx = models.CharField(
        _("SPDX ID"),
        help_text=_("Short identifier specified by https://spdx.org/licenses/"),
        max_length=16,
        unique=True,
        blank=True,
        null=True,
    )
    text = models.TextField(
        _("text"), help_text=_("The main text of the license."), blank=True
    )
    html = models.TextField(
        _("html"), help_text=_("The main text of the license as html."), blank=True
    )
    template = models.TextField(
        _("template"),
        help_text=_("The main text of the license as a template."),
        blank=True,
        null=True,
    )

    urls = models.JSONField(
        _("URLs"),
        help_text=_(
            "A list of URLs that link to an online resource describing the license."
        ),
        default=list,
    )

    def __str__(self):
        # if self.spdx:
        #     return self.spdx
        return self.name

    class Meta:
        verbose_name = _("license")
        verbose_name_plural = _("license")
        db_table = "license_license"

    def save(self, *args, **kwargs):

        if not self.pk and self.spdx:
            self.update_from_spdx()

        return super().save(*args, **kwargs)

    def update_from_spdx(self):
        data = self.fetch_license()
        self.name = data.get("name")
        self.html = data.get("licenseTextHtml")
        self.text = data.get("licenseText")
        self.template = data.get("standardLicenseTemplate")
        self.urls = data.get("seeAlso")
        self.title = data.get("name")

    def fetch_license(self):
        if self.spdx in SPDX_LICENCES.keys():
            url = f"https://spdx.org/licenses/{self.spdx}.json"
            response = requests.get(url)
            return response.json()
        else:
            raise ValueError(
                _(f"'{self.spdx}' is not a valid SPDX license identified.")
            )
