from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ImageCreate(BaseModel):
    item_id: int
    img_url: str

class ImageOut(BaseModel):
    image_id: int
    item_id: int
    img_url: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ImageInfo(BaseModel):
    image_id: int
    image_url: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True
