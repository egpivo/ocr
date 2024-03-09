import asyncio
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from ocr.main import app
from ocr.routers.img_async import job_results, process_image_async

client = TestClient(app)


@pytest.mark.usefixtures("positive_example_imgstring")
def test_process_image_async_successful(positive_example_imgstring):
    job_id = "test_job_id"
    with patch("ocr.routers.img_async.extract_text_from_image") as mock_extract_text:
        mock_extract_text.return_value = "Test Result"
        result = asyncio.run(process_image_async(positive_example_imgstring, job_id))

    assert result == "Test Result"
    assert job_results[job_id]["status"] == "completed"
    assert job_results[job_id]["result"] == "Test Result"


@pytest.mark.usefixtures("positive_example_imgstring")
def test_process_image_async_failed(positive_example_imgstring):
    job_id = "test_job_id"
    with patch("ocr.routers.img_async.extract_text_from_image") as mock_extract_text:
        mock_extract_text.side_effect = Exception("Test Exception")
        with pytest.raises(Exception, match="Test Exception"):
            asyncio.run(process_image_async(positive_example_imgstring, job_id))

    assert job_results[job_id]["status"] == "failed"
    assert "error" in job_results[job_id]


import uuid


@pytest.mark.usefixtures("positive_example_imgstring")
def test_extract_text_async_successful(positive_example_imgstring):
    with patch("ocr.routers.img_async.process_image_async") as mock_process_image:
        # Generate a unique job_id for the mock return value
        unique_job_id = str(uuid.uuid4())
        mock_process_image.return_value = unique_job_id

        response = client.post("/imgasync", json={"data": positive_example_imgstring})

    assert response.status_code == 200
    result = response.json()

    # Retrieve the job_id from the background task
    background_task_job_id = mock_process_image.call_args[0][1]
    assert result == background_task_job_id


@pytest.mark.usefixtures("positive_example_imgstring")
def test_extract_text_async_missing_data_field(positive_example_imgstring):
    response = client.post("/imgasync", json={})
    assert response.status_code == 400
    assert "Missing 'data' field in the request." in response.text


@pytest.mark.usefixtures("positive_example_imgstring")
def test_get_job_result_completed_job(positive_example_imgstring):
    job_id = "completed_job_id"
    job_results[job_id] = {"status": "completed", "result": "Test Result"}

    response = client.get(f"/job/{job_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "completed"
    assert result["result"] == "Test Result"


@pytest.mark.usefixtures("positive_example_imgstring")
def test_get_job_result_pending_job(positive_example_imgstring):
    job_id_pending = "pending_job_id"
    response_pending = client.get(f"/job/{job_id_pending}")
    assert response_pending.status_code == 200
    result_pending = response_pending.json()
    assert result_pending["status"] == "pending"
