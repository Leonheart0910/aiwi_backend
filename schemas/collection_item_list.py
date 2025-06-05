# schemas/collection_item_list.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ImageInfo(BaseModel):
    image_id: int
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class ItemInfo(BaseModel):
    item_id: int
    product_name: str
    product_info: str
    product_link: str
    category_name: str
    created_at: datetime
    image: Optional[ImageInfo]

    class Config:
        from_attributes = True

class CollectionItemList(BaseModel):
    collection_id: int
    collection_title: str
    user_id: int
    created_at: datetime
    items: List[ItemInfo]

    class Config:
        from_attributes = True
