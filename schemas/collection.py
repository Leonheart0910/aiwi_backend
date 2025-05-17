from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class CollectionCreate(BaseModel):
    collection_title: str
    user_id: int

class CollectionOut(BaseModel):
    collection_id: int
    collection_title: str
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True