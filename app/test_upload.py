import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile
from unittest.mock import patch
from application import app
import io

client = TestClient(app)

@pytest.fixture
def test_file():
    return io.BytesIO(b"test image content")

@patch("application.upload_image_to_s3")
@patch("application.save_image_metadata_to_dynamodb")
def test_upload_image(mock_save_to_dynamo, mock_upload_to_s3, test_file):
    mock_upload_to_s3.return_value = True
    mock_save_to_dynamo.return_value = True

    response = client.post(
        "/upload/",
        files={"file": ("test.jpg", test_file, "image/jpeg")},
        data={
            "title": "Test Title",
            "description": "Test Description",
            "tags": "nature,sunset"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["tags"] == ["nature", "sunset"]
    assert data["filename"].endswith("test.jpg")

    mock_upload_to_s3.assert_called_once()
    mock_save_to_dynamo.assert_called_once()