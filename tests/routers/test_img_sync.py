import pytest
from fastapi.testclient import TestClient

from ocr.core.schemas.image import ImageRequest
from ocr.main import app

client = TestClient(app)


@pytest.mark.usefixtures("positive_example_imgstring", "expected_result")
def test_extract_text_from_image_success(positive_example_imgstring, expected_result):
    image_request = ImageRequest(data=positive_example_imgstring)
    # Test with a valid base64 string
    response = client.post("/imgsync", json=image_request.dict())

    assert response.status_code == 200
    result = response.json()

    # Ensure 'extracted_text' is a valid string
    assert isinstance(result["extracted_text"], str)
    # Ensure the result matches the expected result
    assert result["extracted_text"] == expected_result


@pytest.mark.usefixtures("false_example_imgstring")
def test_extract_text_from_image_invalid_data(false_example_imgstring):
    image_request = ImageRequest(data=false_example_imgstring)
    # Test with an invalid base64 string
    response = client.post("/imgsync", json={"data": image_request.dict()})
    assert response.status_code == 422


@pytest.mark.usefixtures("positive_example_imgstring")
def test_extract_text_from_image_missing_data(positive_example_imgstring):
    # Test with missing 'data' field in the request
    response = client.post("/imgsync", json={})
    assert response.status_code == 422
