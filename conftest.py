import pytest

from helper.utility import list_images


@pytest.fixture
def all_images():
    """Lists all images for testing"""
    return list_images("static")
