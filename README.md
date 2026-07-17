# Django Content License

[![Github Build](https://github.com/SamuelJennings/django-content-license/actions/workflows/build.yml/badge.svg)](https://github.com/SamuelJennings/django-content-license/actions/workflows/build.yml)
[![Github Tests](https://github.com/SamuelJennings/django-content-license/actions/workflows/tests.yml/badge.svg)](https://github.com/SamuelJennings/django-content-license/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/SamuelJennings/django-content-license/branch/main/graph/badge.svg)](https://codecov.io/gh/SamuelJennings/django-content-license)
![GitHub](https://img.shields.io/github/license/SamuelJennings/django-content-license)
![GitHub last commit](https://img.shields.io/github/last-commit/SamuelJennings/django-content-license)
<!-- ![PyPI](https://img.shields.io/pypi/v/django-content-license) -->

A Django app that allows you to associate content licenses with model instances and display appropriate attribution in your HTML templates. Perfect for academic datasets, research publications, creative content, and any application where proper licensing and attribution are important.

## Features

- **License Management**: Store and manage various content licenses (MIT, GPL, Creative Commons, etc.)
- **Easy Integration**: Simple `LicenseField` that can be added to any Django model
- **Automatic Attribution**: Render proper HTML attribution snippets via the field's auto-injected `get_<field>_display()` method
- **Template Override**: Customize the attribution markup by shadowing the `licensing/snippet.html` template
- **Validation**: Built-in validation for license consistency and requirements
- **Internationalization**: Full i18n support with translations
- **Performance**: Optimized database queries and indexing

## Scope & philosophy

django-content-license is deliberately small: it stores licenses, attaches them to your
models, and renders attribution where a license needs it. Think of the license picker GitHub
puts on a new repository, plus the attribution some licenses (like Creative Commons) ask you
to show.

It stays generic on purpose. It is not a citation or metadata exporter (BibTeX, DataCite,
CSL), not a license-compatibility checker, and not tied to any one project's needs or to the
Creative Commons attribution style.

When choices collide: generic beats specific, simplicity beats flexibility, and attribution
stays configurable: a license defines what it needs, and one that only needs its title shown
simply doesn't use the feature.

Where it's headed is tracked in [GOALS.md](GOALS.md).

## Quick Start

### Installation

```bash
pip install django-content-license
```

### Settings

Add `licensing` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'licensing',
]
```

Run migrations:

```bash
python manage.py migrate licensing
```

### Basic Usage

#### 1. Add License Field to Your Model

```python
from django.db import models
from licensing.fields import LicenseField

class Dataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    license = LicenseField()  # This field links to a License

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/datasets/{self.pk}/"
```

#### 2. Create Licenses

```python
from licensing.models import License

# Create licenses through Django admin or programmatically
mit_license = License.objects.create(
    name="MIT License",
    canonical_url="https://opensource.org/licenses/MIT",
    description="A permissive license that allows commercial use",
    text="Permission is hereby granted, free of charge..."
)
```

#### 3. Display Attribution in Templates

```html
<!-- In your template -->
<div class="dataset">
    <h2>{{ dataset.name }}</h2>
    <p>{{ dataset.description }}</p>

    <!-- Automatic attribution display -->
    <div class="license-attribution">
        {{ dataset.get_license_display }}
    </div>
</div>
```

This will output properly formatted HTML like:
```html
<a href="/datasets/1/">My Dataset</a> is licensed under
<a href="https://opensource.org/licenses/MIT" target="_blank" rel="noopener">MIT License</a>
```

## Advanced Usage

### Custom License Field Options

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    # Custom license field with specific options
    license = LicenseField(
        verbose_name="Content License",
        help_text="Choose the license for this article",
        on_delete=models.PROTECT,  # Prevent license deletion if referenced
        limit_choices_to={'is_active': True},  # Only show active licenses
    )
```

### Working with Creators/Authors

If your model has creator information, the attribution will automatically include it:

```python
class Research(models.Model):
    title = models.CharField(max_length=200)
    license = LicenseField()

    # The template will automatically look for these fields
    creators = models.CharField(max_length=200)  # Or ForeignKey to User/Author model

    def get_absolute_url(self):
        return f"/research/{self.pk}/"

# In template, this will generate:
# "Research Title by John Doe is licensed under MIT License"
```

### License Model API

```python
from licensing.models import License

# Get all active/recommended licenses
active_licenses = License.get_recommended_licenses()

# Check license properties
license = License.objects.get(name="MIT License")
print(license.status_display)  # "Active" or "Deprecated"
print(license.short_description)  # Truncated description
print(license.full_name)  # Full license name

# Validation
license.clean()  # Validates license consistency
```

### Template Customization

You can override the default attribution template by creating your own `licensing/snippet.html`:

```html
<!-- templates/licensing/snippet.html -->
{% load i18n %}
<div class="license-info">
    {% if object.creators %}
        <span class="creators">By {{ object.creators }}</span>
    {% endif %}
    <span class="license-link">
        Licensed under <a href="{{ license.canonical_url }}" target="_blank" rel="noopener">
            {{ license.name }}
        </a>
    </span>
</div>
```

## Available License Fields

### LicenseField Parameters

- `verbose_name`: Display name for the field (default: "license")
- `help_text`: Help text for admin forms
- `on_delete`: What to do when license is deleted (default: `models.PROTECT`)
- `limit_choices_to`: Limit available license choices
- `null/blank`: Whether field can be empty

### Model Validation

The `License` model includes built-in validation:

```python
# Deprecated licenses must have a deprecated_date
license = License(name="Old License", is_active=False)
license.clean()  # Raises ValidationError

# Active licenses shouldn't have deprecated_date
license = License(
    name="Active License",
    is_active=True,
    deprecated_date=timezone.now().date()
)
license.clean()  # Raises ValidationError
```

## Testing

The suite is written as Django `TestCase` classes and run with pytest (pytest-django).

### Running Tests

```bash
# Run with pytest (settings module: tests.settings)
poetry run pytest

# Run with coverage
poetry run pytest --cov=licensing --cov-report=html
```

### Test Organization

- `tests/test_models.py` - `License` model functionality
- `tests/test_fields.py` - `LicenseField` and attribution rendering
- `tests/test_utils.py` - attribution/utility helpers

### Writing Your Own Tests

```python
import pytest
from licensing.models import License
from licensing.fields import LicenseField

@pytest.mark.django_db
def test_my_model_with_license():
    license_obj = License.objects.create(
        name="Test License",
        canonical_url="https://example.com/license",
        text="License text"
    )

    # Test your model here
    instance = MyModel.objects.create(license=license_obj)
    assert instance.license == license_obj
```

## Admin Integration

The package does **not** register a `ModelAdmin` for you — register `License` in your own
project's `admin.py` so you control the site it appears on and how it's displayed. The model
exposes helpers (`status_display`, `short_description`) that are handy in `list_display`:

```python
# admin.py
from django.contrib import admin
from licensing.models import License

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ['name', 'status_display', 'canonical_url']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'slug']
```

## Performance Considerations

### Database Optimization
- Indexes are automatically created on `is_active` and `slug` fields
- License lookups are optimized using `select_related`
- Slug generation uses efficient bulk queries

### Caching
For high-traffic sites, consider caching license information:

```python
from django.core.cache import cache
from django.db.models.signals import post_save

def invalidate_license_cache(sender, instance, **kwargs):
    cache.delete(f'license_{instance.pk}')

post_save.connect(invalidate_license_cache, sender=License)
```

## Migration from Other Apps

If you're migrating from another licensing solution:

```python
# Create a data migration
from django.db import migrations

def migrate_licenses(apps, schema_editor):
    OldLicense = apps.get_model('old_app', 'License')
    NewLicense = apps.get_model('licensing', 'License')

    for old_license in OldLicense.objects.all():
        NewLicense.objects.create(
            name=old_license.name,
            canonical_url=old_license.url,
            text=old_license.text,
            # Map other fields as needed
        )

class Migration(migrations.Migration):
    dependencies = [
        ('licensing', '0001_initial'),
        ('old_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_licenses),
    ]
```

## Common Use Cases

### Academic Research
```python
class ResearchPaper(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(User)
    license = LicenseField(
        help_text="Choose appropriate license for your research data"
    )

    # For dataset licensing
    dataset_license = LicenseField(
        verbose_name="Dataset License",
        related_name="research_datasets"
    )
```

### Creative Content
```python
class Artwork(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    license = LicenseField(
        limit_choices_to={'name__icontains': 'Creative Commons'}
    )
```

### Software Projects
```python
class SoftwareProject(models.Model):
    name = models.CharField(max_length=200)
    license = LicenseField(
        limit_choices_to={'name__in': ['MIT', 'GPL', 'Apache']}
    )
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/SamuelJennings/django-content-license.git
cd django-content-license

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linting
poetry run black .
poetry run pylint licensing/
```

### Code Quality

We maintain high code quality standards:
- 100% test coverage target
- Type hints for all public APIs
- Comprehensive documentation
- Regular security audits

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: this README (usage) and `docs/adr/` (design decisions)
- **Issues**: Report bugs at [GitHub Issues](https://github.com/SamuelJennings/django-content-license/issues)

## Changelog

See [HISTORY.md](HISTORY.md) for a complete changelog.

## Related Projects

- [Creative Commons – cc-licenses](https://github.com/creativecommons/cc-licenses) - Official CC license data

---

Made with ❤️ by the Django community
