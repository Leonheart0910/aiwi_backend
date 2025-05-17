from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AiwiCreate(BaseModel):
    title: str
    user_id: int

class AiwiOut(BaseModel):
    aiwi_id: int
    title: str
    user_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
