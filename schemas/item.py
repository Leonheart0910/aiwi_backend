from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.dialects.mysql import BIGINT

from schemas.image import ImageOut, ImageInfo


class CreateItem(BaseModel):
    category_name : str
    product_name : str
    product_info : str
    collection_id : int


class ItemOut(BaseModel):
    item_id : int
    category_name : str
    product_name : str
    product_info : str
    collection_id : int
    images: List[ImageOut] = []
    created: Optional[datetime]
    updated: Optional[datetime]
    class Config:
        from_attributes = True

class ItemInfo(BaseModel):
    item_id : int
    product_link : str
    product_name : str
    product_info : str
    category_name: str
    image: List[ImageInfo] = []
    created_at : Optional[datetime]

    class Config:
        from_attributes = True

class ItemSaveRequest(BaseModel):
    user_id: int
    product_id: int
    collection_id : int

