import time
import uuid
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from ocr.core.job_manager import job_results, job_results_lock
from ocr.core.schemas.image import ImageRequest, JobStatusResponse
from ocr.main import app
from ocr.routers.image_async import process_image_async

client = TestClient(app)


@pytest.mark.asyncio
async def test_process_image_async_successful(positive_example_image_string):
    job_id = "test_job_id"
    image_request = ImageRequest(data=positive_example_image_string)
    with patch("ocr.routers.image_async.extract_text_from_image") as mock_extract_text:
        mock_extract_text.return_value = "Test Result"
        result = await process_image_async(image_request, job_id)

    assert result == "Test Result"
    assert job_results[job_id]["status"] == "completed"
    assert job_results[job_id]["extracted_text"] == "Test Result"


@pytest.mark.usefixtures("positive_example_image_string")
async def test_process_image_async_failed(positive_example_image_string):
    job_id = "test_job_id"
    image_request = ImageRequest(data=positive_example_image_string)
    with patch("ocr.routers.image_async.extract_text_from_image") as mock_extract_text:
        mock_extract_text.side_effect = Exception("Test Exception")
        with pytest.raises(
            Exception, match="Test Exception"
        ):  # Adjust the expected message here
            await process_image_async(image_request, job_id)

    assert job_results[job_id]["status"] == "failed"
    assert "error" in job_results[job_id]


@pytest.mark.usefixtures("positive_example_image_string")
def test_extract_text_async_successful(positive_example_image_string):
    image_request = ImageRequest(data=positive_example_image_string)
    with patch("ocr.routers.image_async.process_image_async") as mock_process_image:
        # Generate a unique job_id for the mock return value
        unique_job_id = str(uuid.uuid4())
        mock_process_image.return_value = JobStatusResponse(
            job_id=unique_job_id, status="processing", extracted_text=None
        )

        response = client.post("/imgasync", json=image_request.dict())

    assert response.status_code == 200
    result = response.json()

    # Retrieve the job_id from the background task
    background_task_job_id = mock_process_image.call_args[0][1]
    assert result["job_id"] == background_task_job_id


@pytest.mark.usefixtures("positive_example_image_string")
def test_extract_text_async_missing_data_field(positive_example_image_string):
    response = client.post("/imgasync", json={})
    assert response.status_code == 422
    expected_error_message = "Field required"
    assert expected_error_message in response.json()["detail"][0]["msg"]


@pytest.mark.usefixtures("positive_example_image_string")
def test_get_job_result_completed_job(positive_example_image_string):
    job_id = "completed_job_id"
    # Updated job_results to include "job_id" field
    with job_results_lock:
        job_results[job_id] = {
            "status": "completed",
            "extracted_text": "Test Result",
            "timestamp": time.time(),
        }

    response = client.get(f"/imgasync/job/{job_id}")

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "completed"
    assert result["extracted_text"] == "Test Result"
    assert result["job_id"] == job_id  # Ensure "job_id" is present in the response


@pytest.mark.usefixtures("positive_example_image_string")
def test_get_job_result_pending_job(positive_example_image_string):
    job_id_pending = "pending_job_id"

    # Updated job_results to include "job_id" and "extracted_text" fields
    with job_results_lock:
        job_results[job_id_pending] = {
            "status": "pending",
            "extracted_text": None,
            "timestamp": time.time(),
        }

    response_pending = client.get(f"/imgasync/job/{job_id_pending}")

    assert response_pending.status_code == 200
    result_pending = response_pending.json()
    assert result_pending["status"] == "pending"
    assert result_pending["job_id"] == job_id_pending
    assert result_pending["extracted_text"] is None
