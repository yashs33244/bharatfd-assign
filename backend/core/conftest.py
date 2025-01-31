import pytest
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
