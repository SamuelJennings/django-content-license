"""Upgrading a populated licence table through migration 0002."""

import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

INITIAL = [("licensing", "0001_initial")]
TARGET = [("licensing", "0002_alter_license_options_remove_license_url_and_more")]


@pytest.fixture
def migrate_to():
    """Migrate the licensing app to a target and return the historical License model."""

    def migrate(target):
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(target)
        return executor.loader.project_state(target).apps.get_model("licensing", "License")

    yield migrate
    migrate(MigrationExecutor(connection).loader.graph.leaf_nodes("licensing"))


@pytest.mark.django_db(transaction=True)
class TestMigration0002:
    def test_each_licence_keeps_its_url_as_canonical_url(self, migrate_to):
        License = migrate_to(INITIAL)
        License.objects.create(
            name="MIT", slug="mit", URL="https://opensource.org/licenses/MIT"
        )
        License.objects.create(
            name="GPL",
            slug="gpl",
            URL="https://www.gnu.org/licenses/gpl-3.0.html",
            text="This program is free software",
        )

        License = migrate_to(TARGET)

        assert dict(License.objects.values_list("name", "canonical_url")) == {
            "MIT": "https://opensource.org/licenses/MIT",
            "GPL": "https://www.gnu.org/licenses/gpl-3.0.html",
        }

    def test_a_licence_without_text_gets_empty_text(self, migrate_to):
        License = migrate_to(INITIAL)
        License.objects.create(
            name="MIT", slug="mit", URL="https://opensource.org/licenses/MIT", text=None
        )

        License = migrate_to(TARGET)

        assert License.objects.get(name="MIT").text == ""

    def test_reversing_restores_each_url(self, migrate_to):
        License = migrate_to(TARGET)
        License.objects.create(
            name="MIT",
            slug="mit",
            canonical_url="https://opensource.org/licenses/MIT",
            text="Permission is hereby granted",
        )

        License = migrate_to(INITIAL)

        assert License.objects.get(name="MIT").URL == "https://opensource.org/licenses/MIT"
