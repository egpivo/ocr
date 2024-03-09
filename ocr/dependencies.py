import base64
import io

import pytesseract
from fastapi import HTTPException
from PIL import Image

from ocr.core.schemas.image import ImageResponse
from ocr.logger.logger import logger


def extract_text_from_image(base64_str: str) -> ImageResponse:
    try:
        # Decode Base64 data and open the image
        image_bytes = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_bytes))
        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        return ImageResponse(extracted_text=extracted_text)
    except Exception as e:
        logger.exception("Processing Error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
