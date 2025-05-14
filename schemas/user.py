from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from schemas.user_info import UserInfoCreate


class UserCreate(BaseModel):
    email: str
    nickname: str
    password: str
    user_info: UserInfoCreate

class UserOut(BaseModel):
    user_id: int
    email: str
    nickname: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

