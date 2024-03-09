from typing import List, Optional

from pydantic import BaseModel


class ImageRequest(BaseModel):
    data: str  # Base64-encoded image data


class ImageResponse(BaseModel):
    extracted_text: str


class BatchImageRequest(BaseModel):
    images: List[ImageRequest]


class JobStatusResponse(BaseModel):
    job_id: Optional[str]
    status: str
    extracted_text: Optional[str]
