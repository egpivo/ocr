from fastapi import APIRouter, HTTPException

from ocr.core.schemas.image import ImageRequest, ImageResponse
from ocr.dependencies import extract_text_from_image
from ocr.logger.logger import logger

router = APIRouter()


@router.post("/imgsync", response_model=ImageResponse)
def extract_text_sync(img_data: ImageRequest):
    try:
        base64_image = img_data.data
        if not base64_image:
            logger.error("Missing 'data' field in the request.")
            raise HTTPException(
                status_code=400, detail="Missing 'data' field in the request."
            )

        extracted_text = extract_text_from_image(base64_image)
        return ImageResponse(extracted_text=extracted_text)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Internal Server Error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
