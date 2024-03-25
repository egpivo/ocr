import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException

from ocr.core.job_manager import JobResultsManager
from ocr.core.schemas.image import ImageRequest, JobStatusResponse
from ocr.dependencies import extract_text_from_image
from ocr.routers.utils import handle_errors_and_logging

router = APIRouter()


async def process_image_async(base64_image: str, job_id: str) -> str:
    try:
        extracted_text = extract_text_from_image(base64_image)
        JobResultsManager.update(job_id, "completed", extracted_text=extracted_text)
        return extracted_text
    except Exception as e:
        JobResultsManager.update(job_id, "failed", error=str(e))
        handle_errors_and_logging(e, status_code=500, detail="Internal Server Error")


@router.post("/imgasync", response_model=JobStatusResponse)
async def extract_text_async(
    image_data: ImageRequest, background_tasks: BackgroundTasks
):
    try:
        base64_image = image_data.data
        if not base64_image:
            handle_errors_and_logging(
                None, status_code=400, detail="Missing 'data' field in the request."
            )

        # Generate a unique job_id --> string
        job_id = str(uuid.uuid4())
        # Schedule the image processing in the background
        background_tasks.add_task(process_image_async, base64_image, job_id)

        # Check if extract_text_from_image returns a string or ImageResponse
        return JobStatusResponse(
            job_id=job_id, status="processing", extracted_text=None
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_errors_and_logging(e, status_code=500, detail="Internal Server Error")


@router.get("/imgasync/job/{job_id}", response_model=JobStatusResponse)
async def get_job_result(job_id: str):
    try:
        result = JobResultsManager.get(job_id)

        if not result:
            # If job_id is not found or result has expired, return a response with status pending and job_id as None
            return JobStatusResponse(job_id=None, status="pending", extracted_text=None)

        # Return JobStatusResponse with the result
        return JobStatusResponse(job_id=job_id, **result)
    except Exception as e:
        handle_errors_and_logging(e, status_code=500, detail="Internal Server Error")
