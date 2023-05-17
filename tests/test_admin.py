import pytest
from django.contrib.admin.sites import all_sites
from django.urls import reverse


def get_admin_urls(page):
    """Get all admin URLs."""
    admin_urls = []
    for site in all_sites:
        for model, _model_admin in site._registry.items():
            admin_urls.append(reverse(f"{site.name}:{model._meta.app_label}_{model._meta.model_name}_{page}"))
    return admin_urls


@pytest.mark.parametrize("url", get_admin_urls("changelist"))
def test_admin_changelist_views(url, client, admin_client):
    """Test that admin changelist views return a valid response for admin users and that non-admin users are not allowed.
    """
    assert admin_client.get(url).status_code == 200
    assert client.get(url).status_code != 200


@pytest.mark.parametrize("url", get_admin_urls("add"))
def test_admin_add_views(url, client, admin_client):
    """Test that admin add views return a valid response for admin users and that non-admin users are not allowed."""
    assert admin_client.get(url).status_code == 200
    assert client.get(url).status_code != 200
