import pytest
from fastapi.testclient import TestClient

from ocr.main import app

client = TestClient(app)


@pytest.mark.usefixtures("positive_example_imgstring", "expected_result")
def test_extract_text_from_image_success(positive_example_imgstring, expected_result):
    # Test with a valid base64 string
    response = client.post("/imgsync", json={"data": positive_example_imgstring})
    assert response.status_code == 200
    assert response.json() == {"extracted_text": expected_result}


@pytest.mark.usefixtures("false_example_imgstring")
def test_extract_text_from_image_invalid_data(false_example_imgstring):
    # Test with an invalid base64 string
    response = client.post("/imgsync", json={"data": false_example_imgstring})
    assert response.status_code == 400


@pytest.mark.usefixtures("positive_example_imgstring")
def test_extract_text_from_image_missing_data(positive_example_imgstring):
    # Test with missing 'data' field in the request
    response = client.post("/imgsync", json={})
    assert response.status_code == 400
