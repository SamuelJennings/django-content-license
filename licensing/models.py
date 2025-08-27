from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class License(models.Model):
    name = models.CharField(_("name"), help_text=_("The name of the license"), max_length=255, unique=True)

    canonical_url = models.URLField(
        _("canonical URL"),
        help_text=_("A permanent online resource describing the license"),
        max_length=500,
        unique=True,
    )

    description = models.TextField(
        _("description"),
        help_text=_("A short description of the license"),
        blank=True,
        null=True,
    )

    text = models.TextField(
        _("text"),
        help_text=_("The full text of the license")
    )

    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Whether this license is still recommended for use")
    )

    deprecated_date = models.DateField(
        _("deprecated date"),
        null=True,
        blank=True,
        help_text=_("Date when this license was deprecated")
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    slug = models.SlugField(_("slug"), max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = _("license")
        verbose_name_plural = _("licenses")
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<License: {self.name}>"

    @property
    def full_name(self):
        """Return full license name"""
        return self.name

    @property
    def short_description(self):
        """Truncated description for admin list display"""
        if self.description:
            return (self.description[:100] + '...') if len(self.description) > 100 else self.description
        return _("No description")

    @property
    def status_display(self):
        """Human-readable status for admin"""
        if not self.is_active:
            return _("Deprecated")
        return _("Active")

    def clean(self):
        """Validate the model fields."""
        super().clean()

        # Validate that deprecated licenses have a deprecated_date
        if not self.is_active and not self.deprecated_date:
            raise ValidationError({
                'deprecated_date': _('Deprecated licenses must have a deprecated date.')
            })

        # Validate that active licenses don't have a deprecated_date
        if self.is_active and self.deprecated_date:
            raise ValidationError({
                'deprecated_date': _('Active licenses should not have a deprecated date.')
            })

    @classmethod
    def get_recommended_licenses(cls):
        """Get currently recommended licenses"""
        return cls.objects.filter(is_active=True).order_by('name')

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            base_slug = slugify(self.name)
            if not base_slug:  # Handle edge case where name doesn't generate a valid slug
                base_slug = 'license'

            # Ensure unique slug with optimized query
            slug = base_slug
            counter = 1
            queryset = License.objects.filter(slug__startswith=base_slug)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            existing_slugs = set(queryset.values_list('slug', flat=True))

            while slug in existing_slugs:
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
