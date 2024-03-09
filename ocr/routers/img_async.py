import asyncio

from fastapi import APIRouter, BackgroundTasks, HTTPException

from ocr.dependencies import extract_text_from_image

router = APIRouter()

# In-memory storage for job results
job_results = {}


async def process_image_async(base64_image: str) -> str:
    return extract_text_from_image(base64_image)


@router.post("/imgasync")
async def extract_text_async(img_data: dict, background_tasks: BackgroundTasks):
    try:
        base64_image = img_data.get("data", "")
        if not base64_image:
            raise HTTPException(
                status_code=400, detail="Missing 'data' field in the request."
            )

        # Schedule the image processing in the background and return a job ID
        job_id = await run_in_background(
            background_tasks, process_image_async, base64_image
        )
        return {"job_id": job_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/job/{job_id}")
async def get_job_result(job_id: str):
    try:
        # Retrieve the result or status of the job from the in-memory storage
        if job_id in job_results:
            return job_results[job_id]
        else:
            return {"status": "pending"}
    except Exception as e:
        print(f"Error getting job result: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def run_in_background(background_tasks: BackgroundTasks, func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    job_id = str(hash((func, args, frozenset(kwargs.items()))))
    task = loop.create_task(run_function(job_id, func, *args, **kwargs))
    background_tasks.add_task(lambda: task)
    return job_id


async def run_function(job_id, func, *args, **kwargs):
    try:
        result = await func(*args, **kwargs)
        # Store the result in the in-memory storage
        job_results[job_id] = {"status": "completed", "result": result}
    except Exception as e:
        job_results[job_id] = {"status": "failed", "error": str(e)}
