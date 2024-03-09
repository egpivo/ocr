import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException

from ocr.dependencies import extract_text_from_image
from ocr.logger.logger import logger

router = APIRouter()

# In-memory storage for job results
job_results = {}


async def process_image_async(base64_image: str, job_id: str) -> str:
    try:
        result = extract_text_from_image(base64_image)  # Call synchronously
        job_results[job_id] = {"status": "completed", "result": result}
        return result
    except Exception as e:
        job_results[job_id] = {"status": "failed", "error": str(e)}
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


@router.post("/imgasync")
async def extract_text_async(img_data: dict, background_tasks: BackgroundTasks) -> str:
    try:
        base64_image = img_data.get("data", "")
        if not base64_image:
            logger.error("Missing 'data' field in the request.")
            raise HTTPException(
                status_code=400, detail="Missing 'data' field in the request."
            )
        # Generate a unique job_id
        job_id = str(uuid.uuid4())
        # Schedule the image processing in the background
        background_tasks.add_task(process_image_async, base64_image, job_id)
        return job_id
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Internal Server Error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/imgasync/job/{job_id}")
async def get_job_result(job_id: str):
    try:
        # Retrieve the result or status of the job from the in-memory storage
        return job_results.get(job_id, {"status": "pending"})
    except Exception as e:
        print(f"Error getting job result: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error")
