import pytest
from fastapi.testclient import TestClient

from ocr.main import app

client = TestClient(app)


@pytest.mark.usefixtures("positive_example_imgstring")
def test_extract_text_async(positive_example_imgstring):
    response = client.post("/imgasync", json={"data": positive_example_imgstring})
    assert response.status_code == 200
    result = response.json()
    assert "job_id" in result  # Ensure the response contains a job_id

    # Add more specific tests based on the expected behavior of the /imgasync endpoint
    # For example, check for valid job_id format or expected status codes
