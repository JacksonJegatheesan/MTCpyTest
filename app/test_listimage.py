import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from application import app

client = TestClient(app)

@patch("application.get_image_by_id")
@patch("application.delete_file_from_s3")
@patch("application.delete_metadata_from_dynamodb")
def test_delete_image_204(mock_delete_dynamo, mock_delete_s3, mock_get_image):
    # Setup test data
    image_id = "test-id-001"
    mock_image = {
        "id": image_id,
        "filename": "test-id-001_file.jpg",
        "title": "To be deleted",
        "description": "Mock description",
        "tags": ["tag1"]
    }

    mock_get_image.return_value = mock_image
    mock_delete_s3.return_value = True
    mock_delete_dynamo.return_value = True

    # Send DELETE request
    response = client.delete(f"/images/{image_id}")

    # Assertions
    assert response.status_code == 204
    assert response.content == b""  # 204 must return empty

    mock_get_image.assert_called_once_with(image_id)
    mock_delete_s3.assert_called_once_with("uploads", mock_image["filename"])
    mock_delete_dynamo.assert_called_once_with(image_id)