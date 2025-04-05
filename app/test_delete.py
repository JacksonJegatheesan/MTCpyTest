import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from application import app

client = TestClient(app)

@patch("application.get_image_by_id")
@patch("application.delete_file_from_s3")
@patch("application.delete_metadata_from_dynamodb")
def test_delete_image(
    mock_delete_metadata,
    mock_delete_s3,
    mock_get_image
):
    # Setup mock return value for get_image_by_id
    image_id = "abc-123"
    mock_image = {
        "id": image_id,
        "filename": "abc-123_test.jpg",
        "title": "Test",
        "description": "Test image",
        "tags": ["test"]
    }
    mock_get_image.return_value = mock_image
    mock_delete_s3.return_value = True
    mock_delete_metadata.return_value = True

    response = client.delete(f"/images/{image_id}")

    assert response.status_code == 204
    # if No content response body should be empty
    assert response.content == b""

    mock_get_image.assert_called_once_with(image_id)
    mock_delete_s3.assert_called_once_with("uploads", mock_image["filename"])
    mock_delete_metadata.assert_called_once_with(image_id)