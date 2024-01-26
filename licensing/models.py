from django.db import models
from django.utils.encoding import force_str
from django.utils.text import slugify
from django.utils.translation import gettext as _


class License(models.Model):
    name = models.CharField(_("name"), help_text=_("The name of the license"), max_length=255, unique=True)

    URL = models.URLField(
        _("canonical URL"),
        help_text=_("A permanent online resource describing the license"),
        max_length=200,
        unique=True,
    )

    description = models.TextField(
        _("description"), help_text=_("A short description of the license"), null=True, blank=True
    )

    text = models.TextField(_("text"), help_text=_("The full text of the license"), null=True, blank=True)

    slug = models.SlugField(_("slug"), max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = _("license")
        verbose_name_plural = _("licenses")

    def __str__(self):
        return force_str(self.name)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
