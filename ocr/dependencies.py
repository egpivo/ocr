import base64
import io
from binascii import Error as BinasciiError

import pytesseract
from fastapi import HTTPException
from PIL import Image, UnidentifiedImageError

from ocr.logger.logger import logger


def convert_baseb4_str(base64_str: str) -> bytes:
    image_bytes = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(image_bytes))


def is_valid_image(base64_str: bytes) -> bool:
    try:
        _ = convert_baseb4_str(base64_str)
        return True
    except (BinasciiError, UnidentifiedImageError):
        return False


def extract_text_from_image(base64_str: str) -> str:
    if not is_valid_image(base64_str):
        raise HTTPException(status_code=400, detail="Invalid image format.")

    try:
        image = convert_baseb4_str(base64_str)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except (BinasciiError, UnidentifiedImageError, HTTPException) as e:
        logger.exception("Processing Error: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
