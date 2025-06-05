from pydantic import BaseModel
from datetime import datetime
from typing import List

class CollectionOut(BaseModel):
    collection_id: int
    collection_title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ItemOut(BaseModel):
    item_id: int
    item_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    user_id: int
    collection: List[CollectionOut]
    item: List[ItemOut]
