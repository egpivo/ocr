import base64
import io

import pytesseract
from fastapi import HTTPException
from PIL import Image


def extract_text_from_image(base64_str: str) -> str:
    try:
        # Decode Base64 data and open the image
        image_bytes = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_bytes))
        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
