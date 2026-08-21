"""Tests for the LicenseField and template functionality in django-content-license."""

import pytest
from django.db import models
from django.template import Context, Template

from licensing.fields import LicenseField
from licensing.models import License
from tests.factories import LicenseFactory


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


class TestLicenseField:
    """Basic construction and deconstruction behaviour of LicenseField."""

    def test_defaults(self):
        field = LicenseField()

        assert field.remote_field.model == "licensing.License"
        assert field.remote_field.on_delete == models.PROTECT
        # verbose_name and help_text are lazy strings, so compare their str()
        assert str(field.verbose_name) == "license"
        assert (
            str(field.help_text) == "The license under which this content is published"
        )

    def test_custom_values(self):
        field = LicenseField(
            on_delete=models.CASCADE,
            verbose_name="Custom License",
            help_text="Custom help text",
        )

        assert field.remote_field.on_delete == models.CASCADE
        assert str(field.verbose_name) == "Custom License"
        assert str(field.help_text) == "Custom help text"

    def test_init_with_all_kwargs(self):
        field = LicenseField(
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="licensed_objects",
            db_index=True,
            verbose_name="Custom License Field",
            help_text="Custom help for license field",
        )

        assert field.remote_field.on_delete == models.SET_NULL
        assert field.null
        assert field.blank
        assert field.remote_field.related_name == "licensed_objects"
        assert field.db_index
        assert str(field.verbose_name) == "Custom License Field"
        assert str(field.help_text) == "Custom help for license field"

    def test_deconstruct(self):
        field = LicenseField(
            verbose_name="My License",
            help_text="Select a license",
            on_delete=models.CASCADE,
        )

        name, path, args, kwargs = field.deconstruct()

        assert path == "licensing.fields.LicenseField"
        assert "verbose_name" in kwargs
        assert "help_text" in kwargs
        assert "on_delete" in kwargs


class TestLicenseFieldOnDelete:
    """on_delete defaulting and overriding."""

    @pytest.mark.parametrize(
        ("on_delete_kwarg", "expected"),
        [
            (None, models.PROTECT),
            (models.CASCADE, models.CASCADE),
        ],
    )
    def test_on_delete(self, on_delete_kwarg, expected):
        field = (
            LicenseField(on_delete=on_delete_kwarg)
            if on_delete_kwarg
            else LicenseField()
        )

        assert field.remote_field.on_delete == expected


class TestLicenseFieldModelResolution:
    """The 'to' parameter is always forced to the License model."""

    def test_model_resolution(self):
        field = LicenseField()

        assert field.remote_field.model == "licensing.License"

    def test_to_override_with_positional_args(self):
        field = LicenseField(on_delete=models.CASCADE)

        assert field.remote_field.model == "licensing.License"
        assert field.remote_field.on_delete == models.CASCADE

    def test_to_parameter_always_overridden(self):
        field = LicenseField()

        assert field.remote_field.model == "licensing.License"


class TestLicenseFieldAttributes:
    """Attribute pass-through for LicenseField."""

    def test_attributes_set_correctly(self):
        field = LicenseField(null=True, blank=True, db_index=True)

        assert field.null
        assert field.blank
        assert field.db_index
        assert field.remote_field.model == "licensing.License"


class TestLicenseFieldInheritance:
    """LicenseField's relationship to ForeignKey and abstract base models."""

    def test_inherits_from_foreign_key(self):
        field = LicenseField()

        assert isinstance(field, models.ForeignKey)
        assert hasattr(field, "remote_field")
        assert hasattr(field, "related_model")

    def test_with_abstract_base_class(self):
        class BaseModel(models.Model):
            name = models.CharField(max_length=100)

            class Meta:
                abstract = True

        class LicensedModel(BaseModel):
            license = LicenseField()

            class Meta:
                app_label = "test"

        assert hasattr(LicensedModel, "get_license_display")


class TestLicenseFieldContributeToClass:
    """contribute_to_class adds a get_<field>_display method to the model."""

    def test_adds_display_method(self):
        class TestModel(models.Model):
            license = LicenseField()

            class Meta:
                app_label = "licensing"

        assert hasattr(TestModel, "get_license_display")
        assert callable(TestModel.get_license_display)

    def test_does_not_override_existing_method(self):
        class CustomDisplayModel(models.Model):
            license = LicenseField()

            def get_license_display(self):
                return "Custom display method"

            class Meta:
                app_label = "test"

        instance = CustomDisplayModel()
        assert instance.get_license_display() == "Custom display method"

    def test_different_field_name(self):
        class ContentLicensedModel(models.Model):
            content_license = LicenseField()

            class Meta:
                app_label = "test"

        assert hasattr(ContentLicensedModel, "get_content_license_display")
        assert callable(ContentLicensedModel.get_content_license_display)


@pytest.fixture
def cc_by_license():
    """The Creative Commons BY 4.0 licence shared by the attribution template tests."""
    return LicenseFactory(
        name="Creative Commons BY 4.0",
        canonical_url="https://creativecommons.org/licenses/by/4.0/",
        text="CC BY license text",
        description="Allows others to distribute and build upon the material",
    )


class TestLicenseAttributionTemplate:
    """Rendering of the license attribution blocktrans template."""

    def test_with_all_attributes(self, cc_by_license):
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

        context = Context({"object": mock_object, "license": cc_by_license})

        rendered = template.render(context).strip()

        assert 'href="/object/1/"' in rendered
        assert "My Article" in rendered
        assert 'href="/creator/1/"' in rendered
        assert "Jane Doe" in rendered
        assert 'href="https://creativecommons.org/licenses/by/4.0/"' in rendered
        assert "Creative Commons BY 4.0" in rendered
        assert 'target="_blank"' in rendered

    def test_object_with_url_no_creators(self, cc_by_license):
        mock_object = MockModel("My Article", has_url=True, creators=None)

        template = Template("""
        {% load i18n %}
        {% if object.get_absolute_url %}
            {% blocktrans with object_url=object.get_absolute_url object_name=object license_url=license.canonical_url license_name=license.name %}
<a href="{{ object_url }}">{{ object_name }}</a> is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
            {% endblocktrans %}
        {% endif %}
        """)

        context = Context({"object": mock_object, "license": cc_by_license})

        rendered = template.render(context).strip()

        assert 'href="/object/1/"' in rendered
        assert "My Article" in rendered
        assert (
            " by " not in rendered
        )  # No creator mentioned (check for word boundaries)
        assert 'href="https://creativecommons.org/licenses/by/4.0/"' in rendered
        assert "Creative Commons BY 4.0" in rendered

    def test_object_with_creators_no_url(self, cc_by_license):
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

        context = Context({"object": mock_object, "license": cc_by_license})

        rendered = template.render(context).strip()

        assert "My Book" in rendered
        assert "by John Smith" in rendered
        assert 'href="/object/' not in rendered  # No object URL
        assert 'href="/creator/' not in rendered  # No creator URL
        assert 'href="https://creativecommons.org/licenses/by/4.0/"' in rendered

    def test_minimal_object(self, cc_by_license):
        mock_object = MockModel("Simple Content", has_url=False, creators=None)

        template = Template("""
        {% load i18n %}
        {% blocktrans with object_name=object license_url=license.canonical_url license_name=license.name %}
{{ object_name }} is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
        {% endblocktrans %}
        """)

        context = Context({"object": mock_object, "license": cc_by_license})

        rendered = template.render(context).strip()

        assert "Simple Content" in rendered
        assert " by " not in rendered  # No creator (check for word boundaries)
        assert 'href="/object/' not in rendered  # No object URL
        assert 'href="https://creativecommons.org/licenses/by/4.0/"' in rendered
        assert "is licensed under" in rendered

    def test_with_different_license(self, cc_by_license, mit_license):
        mock_object = MockModel("My Code")

        template = Template("""
        {% load i18n %}
        {% blocktrans with object_name=object license_url=license.canonical_url license_name=license.name %}
{{ object_name }} is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
        {% endblocktrans %}
        """)

        context = Context({"object": mock_object, "license": mit_license})

        rendered = template.render(context).strip()

        assert "MIT License" in rendered
        assert "https://opensource.org/licenses/MIT" in rendered

    def test_escaping(self, cc_by_license):
        html_license = LicenseFactory(
            name="<script>License</script>",
            canonical_url="https://example.com/html-license",
            text="License with HTML in name",
        )

        mock_object = MockModel("Test Content")

        template = Template("""
        {% load i18n %}
        {% blocktrans with object_name=object license_url=license.canonical_url license_name=license.name %}
{{ object_name }} is licensed under <a href="{{ license_url }}" target="_blank">{{ license_name }}</a>
        {% endblocktrans %}
        """)

        context = Context({"object": mock_object, "license": html_license})

        rendered = template.render(context)

        # Should escape the HTML tags
        assert "&lt;script&gt;License&lt;/script&gt;" in rendered
        assert "<script>License</script>" not in rendered


@pytest.fixture
def apache_license():
    """The Apache 2.0 licence shared by the real-model integration tests."""
    return LicenseFactory(
        name="Apache License 2.0",
        canonical_url="https://www.apache.org/licenses/LICENSE-2.0",
        text="Apache 2.0 license text",
        description="A permissive license with patent protection",
    )


class TestLicenseFieldInRealModel:
    """Integration tests against example.models.TestModel, a real LicenseField user."""

    def test_field_in_real_model(self, apache_license):
        from example.models import TestModel

        test_obj = TestModel.objects.create(content_license=apache_license)

        assert test_obj.content_license == apache_license
        assert test_obj.content_license.name == "Apache License 2.0"

        assert hasattr(test_obj, "get_content_license_display")
        assert callable(test_obj.get_content_license_display)

    def test_on_delete_protect(self, apache_license):
        from example.models import TestModel

        TestModel.objects.create(content_license=apache_license)

        with pytest.raises(Exception):  # ProtectedError
            apache_license.delete()

    def test_cascade_behavior(self, apache_license):
        from example.models import TestModel

        test_obj = TestModel.objects.create(content_license=apache_license)
        test_obj_id = test_obj.id

        test_obj.delete()

        assert License.objects.filter(pk=apache_license.pk).exists()
        assert not TestModel.objects.filter(pk=test_obj_id).exists()

    def test_multiple_models_same_license(self, apache_license):
        from example.models import TestModel

        obj1 = TestModel.objects.create(content_license=apache_license)
        obj2 = TestModel.objects.create(content_license=apache_license)

        assert obj1.content_license == obj2.content_license
        assert obj1.content_license.pk == obj2.content_license.pk

        related_objects = TestModel.objects.filter(content_license=apache_license)
        assert related_objects.count() == 2


class TestLicenseAdmin:
    """License admin display methods."""

    def test_display_methods(self):
        from example.admin import LicenseAdmin

        license_obj = LicenseFactory(
            name="BSD 3-Clause",
            canonical_url="https://opensource.org/licenses/BSD-3-Clause",
            text="BSD license text",
            description="A permissive license similar to MIT but with additional clauses",
            is_active=True,
        )

        admin = LicenseAdmin(License, None)

        name_display = admin.get_name_display(license_obj)
        assert license_obj.name in name_display
        assert "<nobr>" in name_display

        url_display = admin.get_canonical_url_display(license_obj)
        assert license_obj.canonical_url in url_display
        assert "<a href=" in url_display
        assert 'target="_blank"' in url_display

        desc_display = admin.get_description_display(license_obj)
        assert license_obj.description in desc_display

    def test_no_description(self):
        from example.admin import LicenseAdmin

        license_no_desc = LicenseFactory(
            name="Simple License",
            canonical_url="https://example.com/simple",
            text="Simple license text",
            description="",
        )

        admin = LicenseAdmin(License, None)
        desc_display = admin.get_description_display(license_no_desc)

        assert desc_display == "No description"
