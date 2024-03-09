from fastapi import APIRouter, HTTPException

from ocr.core.schemas.image import ImageRequest, ImageResponse
from ocr.dependencies import extract_text_from_image
from ocr.routers.utils import handle_errors_and_logging

router = APIRouter()


@router.post("/imgsync", response_model=ImageResponse)
def extract_text_sync(image_data: ImageRequest):
    try:
        base64_image = image_data.data
        if not base64_image:
            handle_errors_and_logging(
                None, status_code=400, detail="Missing 'data' field in the request."
            )

        extracted_text = extract_text_from_image(base64_image)
        return ImageResponse(extracted_text=extracted_text)
    except HTTPException as e:
        raise e
    except Exception as e:
        handle_errors_and_logging(e, status_code=500, detail="Internal Server Error")
