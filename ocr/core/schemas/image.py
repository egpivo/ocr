from typing import List, Optional

from pydantic import BaseModel


class ImageRequest(BaseModel):
    data: str  # Base64-encoded image data


class ImageResponse(BaseModel):
    extracted_text: str


class BatchImageRequest(BaseModel):
    images: List[ImageRequest]


class JobStatusResponse(BaseModel):
    job_id: Optional[
        str
    ]  # Make the job_id optional since it might not be available immediately
    status: str
    result: Optional[dict]  # Include result as optional if it's not available yet
