import base64
import io

import pytesseract
from fastapi import HTTPException
from PIL import Image

from ocr.logger.logger import logger


def is_valid_image(base64_str: bytes) -> bool:
    try:
        image_bytes = base64.b64decode(base64_str)
        Image.open(io.BytesIO(image_bytes))
        return True
    except Exception:
        return False


def extract_text_from_image(base64_str: str) -> str:
    if not is_valid_image(base64_str):
        raise HTTPException(status_code=400, detail="Invalid image format.")

    try:
        # Decode Base64 data
        image_bytes = base64.b64decode(base64_str)
        # Open the image
        image = Image.open(io.BytesIO(image_bytes))

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        logger.exception("Processing Error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
