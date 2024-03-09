from fastapi import APIRouter, HTTPException

from ocr.dependencies import extract_text_from_image

router = APIRouter()


@router.post("/imgsync")
def extract_text_sync(img_data: dict):
    try:
        base64_image = img_data.get("data", "")
        if not base64_image:
            raise HTTPException(
                status_code=400, detail="Missing 'data' field in the request."
            )

        extracted_text = extract_text_from_image(base64_image)
        return {"extracted_text": extracted_text}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
