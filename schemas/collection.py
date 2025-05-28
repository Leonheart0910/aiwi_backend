from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from typing import List
from schemas.item import ItemOut, ItemInfo


class CollectionCreate(BaseModel):
    collection_title: str
    user_id: int

class CollectionResponse(BaseModel):
    collection_id: int
    collection_title: str
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class CollectionWithItems(BaseModel):
    collection_id: int
    collection_title: str
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    items: List[ItemOut] = []

    class Config:
        from_attributes = True

class CollectionCreateRequest(BaseModel):
    user_id : int
    collection_title: str

class CollectionItemList(BaseModel):
    collection_id: int
    collection_title: str
    user_id: int
    created_at: Optional[datetime]
    items: List[ItemInfo] = []

    class Config:
        from_attributes = True