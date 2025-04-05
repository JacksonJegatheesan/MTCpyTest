import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from application import app

client = TestClient(app)

@patch("application.search_images")
def test_search_images_endpoint(mock_search_images):
    mock_data = [
        {
            "id": "123",
            "filename": "123_test.jpg",
            "title": "Sunset View",
            "description": "A beautiful sunset",
            "tags": ["sunset", "nature"]
        }
    ]
    mock_search_images.return_value = mock_data

    response = client.get("/search", params={"title": "sunset", "tag": "nature"})

    assert response.status_code == 200
    assert response.json() == mock_data
    mock_search_images.assert_called_once_with(
        filename=None,
        title="sunset",
        description=None,
        tag="nature"
    )