from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas.image import ImageInfo


class ProductInfo(BaseModel):
    product_id: int
    product_name: str
    product_link: str
    product_price: float
    rank: int
    image: ImageInfo
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True