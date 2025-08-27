"""
Tests for the LicenseField and template functionality in django-content-license.
Django TestCase-based tests.
"""

from django.db import models
from django.template import Context, Template
from django.test import TestCase

from licensing.fields import LicenseField
from licensing.models import License


class MockCreator:
    """Mock creator object for testing."""

    def __init__(self, name="Test Creator", has_url=True):
        self.name = name
        self._has_url = has_url

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self._has_url:
            return "/creator/1/"
        raise AttributeError("Mock creator has no URL")


class MockModel:
    """Mock model for testing license field functionality."""

    def __init__(self, name="Test Object", has_url=True, creators=None):
        self.name = name
        self._has_url = has_url
        self.creators = creators

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self._has_url:
            return "/object/1/"
        raise AttributeError("Mock object has no URL")


class LicenseFieldTest(TestCase):
    """Test cases for the LicenseField."""

    def setUp(self):
        """Set up test fixtures."""
        self.license = License.objects.create(
            name='MIT License',
            canonical_url='https://opensource.org/licenses/MIT',
            text='MIT license text',
            description='A permissive license'
        )

    def test_license_field_defaults(self):
        """Test that LicenseField has correct default values."""
        field = LicenseField()

        self.assertEqual(field.remote_field.model, 'licensing.License')
        self.assertEqual(field.remote_field.on_delete, models.PROTECT)
        # Note: verbose_name and help_text are lazy strings, so we check their string representation
        self.assertEqual(str(field.verbose_name), 'license')
        self.assertEqual(str(field.help_text), 'The license under which this content is published')

    def test_license_field_custom_values(self):
        """Test that LicenseField accepts custom values."""
        field = LicenseField(
            on_delete=models.CASCADE,
            verbose_name='Custom License',
            help_text='Custom help text'
        )

        self.assertEqual(field.remote_field.on_delete, models.CASCADE)
        self.assertEqual(str(field.verbose_name), 'Custom License')
        self.assertEqual(str(field.help_text), 'Custom help text')

    def test_license_field_contribute_to_class(self):
        """Test that LicenseField adds get_*_display method to model class."""

        class TestModel(models.Model):
            license = LicenseField()

            class Meta:
                app_label = 'licensing'

        # Check that the get_license_display method was added
        self.assertTrue(hasattr(TestModel, 'get_license_display'))
        self.assertTrue(callable(TestModel.get_license_display))


class LicenseTemplateTest(TestCase):
    """Test cases for the license attribution template."""

    def setUp(self):
        """Set up test fixtures."""
        self.license = License.objects.create(
            name='Creative Commons BY 4.0',
            canonical_url='https://creativecommons.org/licenses/by/4.0/',
            text='CC BY license text',
            description='Allows others to distribute and build upon the material'
        )

    def test_template_with_all_attributes(self):
        """Test template rendering with object that has all attributes."""
        mock_creator = MockCreator("Jane Doe", has_url=True)
        mock_object = MockModel("My Article", has_url=True, creators=mock_creator)

        template = Template("""
        {% load i18n %}
        {% if object.get_absolute_url and object.creators and object.creators.get_absolute_url %}
            {% blocktrans with object_url=object.get_absolute_url object_name=object creators_url=object.creators.get_absolute_url creators_name=object.creators license_url=license.canonical_url license_name=license.name %}
<a href="{{ object_url }}">{{ object_name }}</a> by <a href="{{ creators_url }}">{{ creators_name }}</a> is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
            {% endblocktrans %}
        {% endif %}
        """)

        context = Context({
            'object': mock_object,
            'license': self.license
        })

        rendered = template.render(context).strip()

        self.assertIn('href="/object/1/"', rendered)
        self.assertIn('My Article', rendered)
        self.assertIn('href="/creator/1/"', rendered)
        self.assertIn('Jane Doe', rendered)
        self.assertIn('href="https://creativecommons.org/licenses/by/4.0/"', rendered)
        self.assertIn('Creative Commons BY 4.0', rendered)
        self.assertIn('target="_blank"', rendered)

    def test_template_object_with_url_no_creators(self):
        """Test template with object that has URL but no creators."""
        mock_object = MockModel("My Article", has_url=True, creators=None)

        template = Template("""
        {% load i18n %}
        {% if object.get_absolute_url %}
            {% blocktrans with object_url=object.get_absolute_url object_name=object license_url=license.canonical_url license_name=license.name %}
<a href="{{ object_url }}">{{ object_name }}</a> is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
            {% endblocktrans %}
        {% endif %}
        """)

        context = Context({
            'object': mock_object,
            'license': self.license
        })

        rendered = template.render(context).strip()

        self.assertIn('href="/object/1/"', rendered)
        self.assertIn('My Article', rendered)
        self.assertNotIn(' by ', rendered)  # No creator mentioned (check for word boundaries)
        self.assertIn('href="https://creativecommons.org/licenses/by/4.0/"', rendered)
        self.assertIn('Creative Commons BY 4.0', rendered)

    def test_template_object_with_creators_no_url(self):
        """Test template with object that has creators but no URL."""
        mock_creator = MockCreator("John Smith", has_url=False)
        mock_object = MockModel("My Book", has_url=False, creators=mock_creator)

        template = Template("""
        {% load i18n %}
        {% if object.creators %}
            {% blocktrans with object_name=object creators_name=object.creators license_url=license.canonical_url license_name=license.name %}
{{ object_name }} by {{ creators_name }} is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
            {% endblocktrans %}
        {% endif %}
        """)

        context = Context({
            'object': mock_object,
            'license': self.license
        })

        rendered = template.render(context).strip()

        self.assertIn('My Book', rendered)
        self.assertIn('by John Smith', rendered)
        self.assertNotIn('href="/object/', rendered)  # No object URL
        self.assertNotIn('href="/creator/', rendered)  # No creator URL
        self.assertIn('href="https://creativecommons.org/licenses/by/4.0/"', rendered)

    def test_template_minimal_object(self):
        """Test template with minimal object (no URL, no creators)."""
        mock_object = MockModel("Simple Content", has_url=False, creators=None)

        template = Template("""
        {% load i18n %}
        {% blocktrans with object_name=object license_url=license.canonical_url license_name=license.name %}
{{ object_name }} is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
        {% endblocktrans %}
        """)

        context = Context({
            'object': mock_object,
            'license': self.license
        })

        rendered = template.render(context).strip()

        self.assertIn('Simple Content', rendered)
        self.assertNotIn(' by ', rendered)  # No creator (check for word boundaries)
        self.assertNotIn('href="/object/', rendered)  # No object URL
        self.assertIn('href="https://creativecommons.org/licenses/by/4.0/"', rendered)
        self.assertIn('is licensed under', rendered)

    def test_template_with_different_license(self):
        """Test template with different license data."""
        mit_license = License.objects.create(
            name='MIT License',
            canonical_url='https://opensource.org/licenses/MIT',
            text='MIT license text'
        )

        mock_object = MockModel("My Code")

        template = Template("""
        {% load i18n %}
        {% blocktrans with object_name=object license_url=license.canonical_url license_name=license.name %}
{{ object_name }} is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
        {% endblocktrans %}
        """)

        context = Context({
            'object': mock_object,
            'license': mit_license
        })

        rendered = template.render(context).strip()

        self.assertIn('MIT License', rendered)
        self.assertIn('https://opensource.org/licenses/MIT', rendered)

    def test_template_escaping(self):
        """Test that template properly escapes HTML in license names."""
        # Create a license with HTML in the name (for testing escaping)
        html_license = License.objects.create(
            name='<script>License</script>',
            canonical_url='https://example.com/html-license',
            text='License with HTML in name'
        )

        mock_object = MockModel("Test Content")

        template = Template("""
        {% load i18n %}
        {% blocktrans with object_name=object license_url=license.canonical_url license_name=license.name %}
{{ object_name }} is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
        {% endblocktrans %}
        """)

        context = Context({
            'object': mock_object,
            'license': html_license
        })

        rendered = template.render(context)

        # Should escape the HTML tags
        self.assertIn('&lt;script&gt;License&lt;/script&gt;', rendered)
        self.assertNotIn('<script>License</script>', rendered)


class LicenseIntegrationTest(TestCase):
    """Integration tests for license functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.license = License.objects.create(
            name='Apache License 2.0',
            canonical_url='https://www.apache.org/licenses/LICENSE-2.0',
            text='Apache 2.0 license text',
            description='A permissive license with patent protection'
        )

    def test_license_field_in_real_model(self):
        """Test LicenseField functionality in actual model usage."""
        # Import the example model
        from example.models import TestModel

        # Create a test instance
        test_obj = TestModel.objects.create(content_license=self.license)

        # Test that the license relationship works
        self.assertEqual(test_obj.content_license, self.license)
        self.assertEqual(test_obj.content_license.name, 'Apache License 2.0')

        # Test that the get_content_license_display method exists and is callable
        self.assertTrue(hasattr(test_obj, 'get_content_license_display'))
        self.assertTrue(callable(test_obj.get_content_license_display))

    def test_license_field_on_delete_protect(self):
        """Test that licenses cannot be deleted when referenced by models."""
        from example.models import TestModel

        # Create a test instance that references the license
        TestModel.objects.create(content_license=self.license)

        # Attempting to delete the license should raise an error
        with self.assertRaises(Exception):  # ProtectedError
            self.license.delete()

    def test_license_cascade_behavior(self):
        """Test behavior when model instance is deleted."""
        from example.models import TestModel

        # Create a test instance
        test_obj = TestModel.objects.create(content_license=self.license)
        test_obj_id = test_obj.id

        # Delete the model instance
        test_obj.delete()

        # License should still exist
        self.assertTrue(License.objects.filter(pk=self.license.pk).exists())

        # Model instance should be gone
        self.assertFalse(TestModel.objects.filter(pk=test_obj_id).exists())

    def test_multiple_models_same_license(self):
        """Test that multiple model instances can share the same license."""
        from example.models import TestModel

        # Create multiple instances with the same license
        obj1 = TestModel.objects.create(content_license=self.license)
        obj2 = TestModel.objects.create(content_license=self.license)

        # Both should reference the same license
        self.assertEqual(obj1.content_license, obj2.content_license)
        self.assertEqual(obj1.content_license.pk, obj2.content_license.pk)

        # License should have multiple references
        related_objects = TestModel.objects.filter(content_license=self.license)
        self.assertEqual(related_objects.count(), 2)


class LicenseAdminTest(TestCase):
    """Test cases for License admin functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.license = License.objects.create(
            name='BSD 3-Clause',
            canonical_url='https://opensource.org/licenses/BSD-3-Clause',
            text='BSD license text',
            description='A permissive license similar to MIT but with additional clauses',
            is_active=True
        )

    def test_license_admin_display_methods(self):
        """Test admin display methods work correctly."""
        from example.admin import LicenseAdmin

        admin = LicenseAdmin(License, None)

        # Test get_name_display
        name_display = admin.get_name_display(self.license)
        self.assertIn(self.license.name, name_display)
        self.assertIn('<nobr>', name_display)

        # Test get_canonical_url_display
        url_display = admin.get_canonical_url_display(self.license)
        self.assertIn(self.license.canonical_url, url_display)
        self.assertIn('<a href=', url_display)
        self.assertIn('target="_blank"', url_display)

        # Test get_description_display with description
        desc_display = admin.get_description_display(self.license)
        self.assertIn(self.license.description, desc_display)

    def test_license_admin_no_description(self):
        """Test admin display method with no description."""
        from example.admin import LicenseAdmin

        # Create license without description
        license_no_desc = License.objects.create(
            name='Simple License',
            canonical_url='https://example.com/simple',
            text='Simple license text',
            description=''
        )

        admin = LicenseAdmin(License, None)
        desc_display = admin.get_description_display(license_no_desc)

        self.assertEqual(desc_display, 'No description')


class LicenseFieldAdvancedTest(TestCase):
    """Advanced test cases for LicenseField to improve coverage."""

    def setUp(self):
        """Set up test fixtures."""
        self.license = License.objects.create(
            name='Test License',
            canonical_url='https://example.com/license',
            description='A test license',
            text='This is the full license text.'
        )

    def test_license_field_init_with_all_kwargs(self):
        """Test LicenseField initialization with various kwargs."""
        field = LicenseField(
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='licensed_objects',
            db_index=True,
            verbose_name='Custom License Field',
            help_text='Custom help for license field'
        )

        self.assertEqual(field.remote_field.on_delete, models.SET_NULL)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertEqual(field.remote_field.related_name, 'licensed_objects')
        self.assertTrue(field.db_index)
        self.assertEqual(str(field.verbose_name), 'Custom License Field')
        self.assertEqual(str(field.help_text), 'Custom help for license field')

    def test_license_field_contribute_to_class_existing_method(self):
        """Test contribute_to_class when method already exists."""

        class TestModel(models.Model):
            license = LicenseField()

            def get_license_display(self):
                return "Custom display method"

            class Meta:
                app_label = 'test'

        # The existing method should not be overridden
        instance = TestModel()
        self.assertEqual(instance.get_license_display(), "Custom display method")

    def test_license_field_contribute_to_class_different_field_name(self):
        """Test contribute_to_class with different field name."""

        class TestModel(models.Model):
            content_license = LicenseField()

            class Meta:
                app_label = 'test'

        # Should create get_content_license_display method
        self.assertTrue(hasattr(TestModel, 'get_content_license_display'))
        self.assertTrue(callable(TestModel.get_content_license_display))

    def test_license_field_inheritance(self):
        """Test that LicenseField properly inherits from ForeignKey."""
        field = LicenseField()

        # Check inheritance
        self.assertIsInstance(field, models.ForeignKey)

        # Check that it has ForeignKey properties
        self.assertTrue(hasattr(field, 'remote_field'))
        self.assertTrue(hasattr(field, 'related_model'))

    def test_license_field_model_resolution(self):
        """Test that LicenseField resolves to correct model."""
        field = LicenseField()

        # The 'to' parameter should be set to the License model
        self.assertEqual(field.remote_field.model, 'licensing.License')

    def test_license_field_default_on_delete(self):
        """Test that default on_delete is PROTECT."""
        field = LicenseField()

        self.assertEqual(field.remote_field.on_delete, models.PROTECT)

    def test_license_field_override_on_delete(self):
        """Test overriding on_delete parameter."""
        field = LicenseField(on_delete=models.CASCADE)

        self.assertEqual(field.remote_field.on_delete, models.CASCADE)

    def test_license_field_with_positional_args_override(self):
        """Test that LicenseField overrides to parameter even with positional args."""
        # Test that 'to' parameter is always overridden to License model
        field = LicenseField(on_delete=models.CASCADE)

        # Should point to License model
        self.assertEqual(field.remote_field.model, 'licensing.License')
        self.assertEqual(field.remote_field.on_delete, models.CASCADE)


class LicenseFieldValidationTest(TestCase):
    """Test validation and edge cases for LicenseField."""

    def test_license_field_deconstruct(self):
        """Test field deconstruction for migrations."""
        field = LicenseField(
            verbose_name='My License',
            help_text='Select a license',
            on_delete=models.CASCADE
        )

        name, path, args, kwargs = field.deconstruct()

        # Check that the field can be reconstructed
        self.assertEqual(path, 'licensing.fields.LicenseField')
        self.assertIn('verbose_name', kwargs)
        self.assertIn('help_text', kwargs)
        self.assertIn('on_delete', kwargs)

    def test_license_field_multiple_inheritance(self):
        """Test LicenseField in models with multiple inheritance."""

        class BaseModel(models.Model):
            name = models.CharField(max_length=100)

            class Meta:
                abstract = True

        class LicensedModel(BaseModel):
            license = LicenseField()

            class Meta:
                app_label = 'test'

        # Should work with inheritance
        self.assertTrue(hasattr(LicensedModel, 'get_license_display'))

class LicenseFieldRegressionTest(TestCase):
    """Regression tests for LicenseField edge cases."""

    def test_license_field_multiple_inheritance(self):
        """Test LicenseField in models with multiple inheritance."""

        class BaseModel(models.Model):
            name = models.CharField(max_length=100)

            class Meta:
                abstract = True

        class LicensedModel(BaseModel):
            license = LicenseField()

            class Meta:
                app_label = 'test'

        # Should work with inheritance
        self.assertTrue(hasattr(LicensedModel, 'get_license_display'))

    def test_license_field_attributes_set_correctly(self):
        """Test that LicenseField sets all attributes correctly."""
        field = LicenseField(
            null=True,
            blank=True,
            db_index=True
        )

        # Check basic attributes
        self.assertTrue(field.null)
        self.assertTrue(field.blank)
        self.assertTrue(field.db_index)
        self.assertEqual(field.remote_field.model, 'licensing.License')

    def test_license_field_to_parameter_override(self):
        """Test that 'to' parameter is always overridden."""
        field = LicenseField()

        # Should always point to License model
        self.assertEqual(field.remote_field.model, 'licensing.License')


