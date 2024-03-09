import pytest
from fastapi.testclient import TestClient

from ocr.main import app

client = TestClient(app)


@pytest.mark.usefixtures("positive_example_imgstring", "expected_result")
def test_extract_text_from_image(positive_example_imgstring, expected_result):
    # Test with the obtained imgstring_value
    response = client.post("/imgsync", json={"data": positive_example_imgstring})
    assert response.status_code == 200
    assert response.json() == {"extracted_text": expected_result}
